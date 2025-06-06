from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .models import DoubtEntry
from .serializers import DoubtEntrySerializer
from django.conf import settings
import openai
import os
from environment_settings import OPENAI_API_KEY
import requests
# Create your views here.

class AskQuestionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        question_text = request.data.get('question_text')
        subject_category = request.data.get('subject_category', 'GMAT-Uncategorized')
        options = request.data.get('options')
        question_type = request.data.get('question_type')

        if not question_text:
            return Response({'detail': 'question_text is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Format options if present
        options_str = ""
        if options and isinstance(options, dict):
            options_str = "\n".join([f"{k}. {v}" for k, v in options.items()])

        # Prompt engineering
        prompt = (
            "You are an expert GMAT tutor. Your goal is to help GMAT students solve problems and understand concepts clearly and concisely.\n"
        )
        if question_type:
            prompt += f"Question Type: {question_type}\n"
        prompt += f"Student's Question: {question_text}\n"
        if options_str:
            prompt += f"Options:\n{options_str}\n"
        prompt += "Please provide a clear and concise answer, explaining your reasoning."

        openai.api_key = OPENAI_API_KEY
        ai_response = None
        try:
            # response = openai.chat.completions.create(
            #     model="gpt-3.5-turbo",
            #     messages=[{"role": "user", "content": prompt}],
            #     max_tokens=512,
            #     temperature=0.7,
            # )
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            }
            # ai_response = response.choices[0].message.content.strip()
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            response_json = response.json()
            ai_response = response_json.get("choices",[])[0].get("message",{}).get("content","").strip()
        except Exception as e:
            return Response({'detail': f'OpenAI API error: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)

        doubt_entry = DoubtEntry.objects.create(
            user=user,
            question_text=question_text,
            full_prompt_sent=prompt,
            ai_response=ai_response,
            subject_category=subject_category
        )
        serializer = DoubtEntrySerializer(doubt_entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DoubtEntryViewSet(viewsets.ModelViewSet):
    serializer_class = DoubtEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow users to see their own doubts
        return DoubtEntry.objects.filter(user=self.request.user).order_by('-timestamp')

    def perform_create(self, serializer):
        question_text = self.request.data.get('question_text')
        subject_category = self.request.data.get('subject_category', 'GMAT-Uncategorized')
        if not question_text:
            raise serializers.ValidationError({'question_text': 'This field is required.'})
        prompt = (
            f"You are an expert GMAT tutor. Your goal is to help GMAT students solve problems and understand concepts clearly and concisely. "
            f"For quantitative problems, provide step-by-step solutions. For verbal concepts, explain rules and provide examples.\n"
            f"Student's Question: {question_text}\n"
        )
        openai.api_key = os.getenv('OPENAI_API_KEY')
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.7,
            )
            ai_response = response.choices[0].message.content.strip()
        except Exception as e:
            raise serializers.ValidationError({'openai': f'OpenAI API error: {str(e)}'})
        serializer.save(
            user=self.request.user,
            full_prompt_sent=prompt,
            ai_response=ai_response,
            subject_category=subject_category
        )
