import boto3

class IntelligentAssistanceService:
	def __init__(self, assistant_name: str) -> None:
		self.client = boto3.client('lexv2-runtime')
		self.assistant_name = assistant_name

	def send_user_text(self, user_id: str, input_text: str):
		response = self.client.recognize_text(
			botId= self.assistant_name,
			botAliasId= 'ContactAssistantLexBot',
			userId= user_id,
			text= input_text
		)

		return response['message']
