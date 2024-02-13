from discord import ButtonStyle, ApplicationContext
from discord.ui import Button, View, button

class Confirm(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.is_confirm: bool = False
    
    @button(label="확인", style=ButtonStyle.green)
    async def confirm(self, interaction: ApplicationContext, _: Button[View]):
        self.is_confirm = True

        await interaction.response.defer()
        self.stop()

    @button(label="취소", style=ButtonStyle.red)
    async def cancel(self, interaction: ApplicationContext, _: Button[View]):
        self.is_confirm = False

        await interaction.response.defer()
        self.stop()