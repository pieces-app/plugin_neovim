import threading
from pieces_os_client import OSApi,AllocationsApi, UserProfile
from typing import Optional
from .settings import Settings

class Auth:
	user_profile:Optional[UserProfile] = None
	
	@classmethod
	def on_user_callback(cls,user):
		cls.user_profile = user

	def login(self):
		thread = OSApi(Settings.api_client).sign_into_os(async_req=True)
		
		def run_allocation_async():
			try:
				thread.get(120)
				self.connect
			except:
				pass
		
		t = threading.Thread(target=run_allocation_async)
		t.start()



	def logout(self):
		OSApi(Settings.api_client).sign_out_of_os(async_req=True)

	def connect(self):
		user = self.user_profile
		if user: # User logged in
			AllocationsApi(Settings.api_client).allocations_connect_new_cloud(user,async_req=True)

	def disconnect(self):
		if self.user_profile and self.user_profile.allocation: # Check if there is an allocation iterable
				AllocationsApi(Settings.api_client).allocations_disconnect_cloud(self.user_profile.allocation,async_req=True)
