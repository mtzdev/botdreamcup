import discord
from discord.ext import commands, tasks
from discord.ext.commands import bot, cooldown, BucketType
from discord.utils import get
from itertools import cycle
from threading import Thread
import asyncio
import json
from datetime import datetime

with open('settings.json', 'r') as cf:
    config = json.loads(cf.read())
    token = config['token']
    prefix = config['prefix']
intents = discord.Intents().all()
client = commands.Bot(command_prefix = prefix, case_insensitive = True, help_command=None, intents=intents)

status = cycle(['Dreamcup League','Campeonatos de CS:GO','Developed by mtz#9765'])

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_ready():
    print('Bot está online!\n')
    change_status.start()

@client.event
async def on_member_join(member):
    cargo = get(member.guild.roles, id=717810679192748072)
    await member.add_roles(cargo)
    log = client.get_channel(717811612311879732)
    await log.send(f'**{member.mention} entrou no servidor**\nConta criada em: {member.created_at}')

@client.event
async def on_member_remove(member):
    log = client.get_channel(717811612311879732)
    await log.send(f'**{member.mention} saiu do servidor.**')

@client.command()
@commands.guild_only()
@commands.cooldown(1,120, commands.BucketType.user)
async def suporte(ctx):
    if ctx.channel.id == 883196216605823006:
        canalsup = await ctx.guild.create_text_channel(f'sup-{ctx.author.discriminator}', category = client.get_channel(id=883201218808266772), overwrites=perms)
        await ctx.message.delete()
        await ctx.send(f'{ctx.author.mention} Ticket de suporte criado! {canalsup.mention}', delete_after=3.0)
        await canalsup.send(f'{ctx.author.mention}',delete_after=0.5)
        embed = discord.Embed(title='Sistema de Tickets de Suporte', description=f'**Olá {ctx.author.mention}!\n\nDescreva sua dúvida ou seu problema abaixo\n\nEm breve um membro da staff realizará o atendimento!**', color=0xff0000)
        embed.set_footer(text='DreamCup League')
        embed.timestamp = datetime.utcnow()
        await canalsup.send(embed=embed)
    else:
        await ctx.send(f'{ctx.author.mention} Você só pode executar este comando dentro do <#883196216605823006>.', delete_after=8.0)
        await ctx.message.delete()
        ctx.command.reset_cooldown(ctx) 

@client.command()
@commands.guild_only()
async def infopause(ctx):
    await ctx.send(f'{ctx.author.mention}\nTodos os campeonatos contam com o sistema de pause dentro do jogo, e nós temos 2 tipos.\n\nPause tático: Para fins táticos, cada equipe tem 4 deles, sendo cada um 30 segundos, e para utiliza-lo basta iniciar a votação de pausa do próprio CS:GO.\n\nPause técnico: É usado para problemas tecnicos, sendo cada equipe com 5 minutos e para usa-lo basta digitar !pause no chat (Após isso informar o problema dentro do chat do jogo no discord).')

@client.command()
@commands.guild_only()
async def infocamp(ctx):
    await ctx.send(f'{ctx.author.mention}\nEste tipo de campeonato é totalmente gratuito, e as premiações são em um sistema de pontos, que funcionam assim:\n\nO campeonato terá um valor em pontos de premiação, o time que ganhar, terá os pontos divididos entre a sua equipe (a divisão é organizada de acordo com o dono responsável pelo time) e após isso você pode digitar !loja e verificar os produtos e fazer a troca pelos pontos por um produto real!\n\nPara verificar quantos pontos você tem digite !pontos.')

@client.command()
@commands.guild_only()
async def help(ctx):
    embed = discord.Embed(title="Lista de Comandos", description="**!suporte**: Faz um ticket de suporte\n**!infocamp**: Mostra as informações do campeonato atual.\n**!infopause:** Mostra as informações sobre o sistema de pause.\n**!loja**: Vê os produtos disponíveis para comprar com pontos.\n**!pontos**: Mostra quantos pontos você tem.\n**!transferir**: Transfere pontos para uma pessoa.", color=0xff0000)
    embed.set_footer(text='Dreamcup League')
    await ctx.send(embed=embed)

@client.command(aliases=['points', 'pontos'])
@commands.guild_only()
async def dinheiro(ctx, pessoa: discord.Member=None):
    if not pessoa:
        await open_account(ctx.author)
        users = await info_pontos_bank()
        quantia = users[str(ctx.author.id)]["pontos"]
        await ctx.send(f'{ctx.author.mention} Você possui {quantia} pontos!')
    else:
        await open_account(pessoa)
        users = await info_pontos_bank()
        quantia = users[str(pessoa.id)]["pontos"]
        await ctx.send(f'O {pessoa.mention} possui {quantia} pontos no momento!')

client.run(token)