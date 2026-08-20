import discord
import math

class Paginator(discord.ui.View):
	current_page = 1
	separator = 20
	data = [] # list of strings
	title:str = ""
	subtitle:str = ""

	def set(self, title:str, subtitle:str, data:list):
		self.title = title
		self.subtitle = subtitle
		self.data = data

	async def send(self, interaction:discord.Interaction):
		self.message = await interaction.followup.send(view=self)
		await self.update_message(self.data[:self.separator])

	def create_embed(self, data:list):
		embed = discord.Embed(title=self.title)
		embed.set_footer(text=f"Page {self.current_page} of {self.max_page_number()}")
		items = "\n".join(data)
		embed.add_field(name=self.subtitle, value=items, inline=False)
		return embed

	async def update_message(self, data:list):
		self.update_buttons()
		await self.message.edit(embed=self.create_embed(data), view=self)
	
	def update_buttons(self):
		if self.current_page <= 1:
			self.first_page.disabled = True
			self.previous_page.disabled = True
			self.first_page.style = discord.ButtonStyle.gray
			self.previous_page.style = discord.ButtonStyle.gray
		else:
			self.first_page.disabled = False
			self.previous_page.disabled = False
			self.first_page.style = discord.ButtonStyle.secondary
			self.previous_page.style = discord.ButtonStyle.primary
		
		if self.current_page >= self.max_page_number():
			self.next_page.disabled = True
			self.last_page.disabled = True
			self.next_page.style = discord.ButtonStyle.gray
			self.last_page.style = discord.ButtonStyle.gray
		else:
			self.next_page.disabled = False
			self.last_page.disabled = False
			self.next_page.style = discord.ButtonStyle.primary
			self.last_page.style = discord.ButtonStyle.secondary

	def get_current_page_data(self):
		item_until = self.current_page * self.separator
		item_from = item_until - self.separator
		if self.current_page == 1:
			item_from = 0 # just make sure
		if self.current_page > self.max_page_number():
			item_until = len(self.data)
		return self.data[item_from:item_until]

	def max_page_number(self):
		return max(1, math.ceil(len(self.data) / self.separator))	

	@discord.ui.button(label="First", style=discord.ButtonStyle.secondary)
	async def first_page(self, interaction:discord.Interaction, button:discord.ui.Button):
		await interaction.response.defer()
		self.current_page = 1
		await self.update_message(self.get_current_page_data())

	@discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
	async def previous_page(self, interaction:discord.Interaction, button:discord.ui.Button):
		await interaction.response.defer()
		self.current_page -= 1
		await self.update_message(self.get_current_page_data())

	@discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
	async def next_page(self, interaction:discord.Interaction, button:discord.ui.Button):
		await interaction.response.defer()
		self.current_page += 1
		await self.update_message(self.get_current_page_data())

	@discord.ui.button(label="Last", style=discord.ButtonStyle.secondary)
	async def last_page(self, interaction:discord.Interaction, button:discord.ui.Button):
		await interaction.response.defer()
		self.current_page = self.max_page_number()
		await self.update_message(self.get_current_page_data())