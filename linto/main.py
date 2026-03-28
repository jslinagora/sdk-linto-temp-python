from .services.studioApiService import StudioApiService
from .services.pollingService import PollingService
from .services.summaryPollingService import SummaryPollingService
from datetime import datetime


class LinTO:
    def __init__(self, auth_token, base_url="https://studio.linto.ai/cm-api"):
        self.base_url = base_url
        self.api_service = StudioApiService(
            base_url=base_url, token=auth_token
        )

    async def transcribe(self, file, enable_diarization=True, number_of_speaker="0", language="*", enablePunctuation=True, name=f"imported file {datetime.now().isoformat()}"):
        args = {}
        args["file"] = file
        res = await self.api_service.upload_file(
            file=file,
            enable_diarization=enable_diarization,
            number_of_speaker=number_of_speaker,
            language=language,
            enablePunctuation=enablePunctuation,
            name=name
        )
        media_id = res["conversationId"]
        return PollingService(media_id, self.api_service)

    async def list_services(self):
        return await self.api_service.fetch_asr_services()

    async def list_llm_services(self):
        """List available LLM services."""
        return await self.api_service.fetch_llm_services()

    async def summarize(self, conversation_id, service_route, flavor=None):
        """Trigger LLM summary and return a polling handle.

        Returns a SummaryPollingService emitting "done", "error", "update" events.
        """
        await self.api_service.trigger_summary(
            conversationId=conversation_id,
            format=service_route,
            flavor=flavor,
        )
        return SummaryPollingService(
            conversation_id, service_route, self.api_service
        )

    async def get_export_list(self, conversation_id):
        """Get list of exports for a conversation."""
        return await self.api_service.get_export_list(
            conversationId=conversation_id
        )

    async def get_export_content(self, conversation_id, job_id):
        """Get the content of a completed export."""
        return await self.api_service.get_export_content(
            conversationId=conversation_id,
            jobId=job_id,
        )

    async def share_conversation(self, conversation_id, email, right=1):
        """Share a conversation with a user by email (READ access by default).

        LinTO Studio sends the notification email automatically.
        """
        return await self.api_service.share_conversation(
            conversationId=conversation_id, email=email, right=right
        )
