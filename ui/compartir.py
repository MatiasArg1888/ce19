import asyncio
from pathlib import Path
from urllib.parse import quote

import flet as ft
from flet.controls.services.url_launcher import LaunchMode


def _snack(page, mensaje):
    try:
        page.snack_bar = ft.SnackBar(ft.Text(mensaje))
        page.snack_bar.open = True
        page.update()
    except Exception:
        pass


def _programar(page, tarea, *args):
    try:
        if hasattr(page, "run_task"):
            futuro = page.run_task(tarea, *args)

            def avisar_error(resultado):
                try:
                    error = resultado.exception()
                except Exception:
                    error = None

                if error:
                    _snack(page, "No se pudo abrir el panel de compartir.")

            try:
                futuro.add_done_callback(avisar_error)
            except Exception:
                pass

            return True
    except Exception:
        pass

    try:
        if hasattr(page, "run_thread"):
            page.run_thread(lambda: asyncio.run(tarea(*args)))
            return True
    except Exception:
        pass

    return False


def _obtener_url_launcher(page):
    launcher = getattr(page, "_codigo19_url_launcher", None)

    if launcher is not None:
        return launcher

    launcher = ft.UrlLauncher()
    setattr(page, "_codigo19_url_launcher", launcher)

    try:
        page.services.append(launcher)
        page.update()
    except Exception:
        pass

    return launcher


async def _abrir_url_async(page, url, modo=LaunchMode.EXTERNAL_APPLICATION):
    launcher = _obtener_url_launcher(page)

    try:
        await launcher.launch_url(url, mode=modo)
        return True
    except Exception:
        pass

    try:
        await launcher.launch_url(url, mode=LaunchMode.EXTERNAL_APPLICATION)
        return True
    except Exception:
        pass

    try:
        await page.launch_url(url, web_popup_window=True)
        return True
    except Exception:
        _snack(page, "No se pudo abrir el enlace.")
        return False


def _abrir_url(page, url, modo=LaunchMode.EXTERNAL_APPLICATION):
    return _programar(page, _abrir_url_async, page, url, modo)


async def _copiar_texto_async(page, texto, mensaje="Contenido copiado."):
    try:
        clipboard = getattr(page, "clipboard", None)

        if clipboard and hasattr(clipboard, "set"):
            await clipboard.set(str(texto))
            _snack(page, mensaje)
            return True
    except Exception:
        pass

    _snack(page, "No se pudo copiar el contenido.")
    return False


def _copiar_texto(page, texto, mensaje="Contenido copiado."):
    return _programar(page, _copiar_texto_async, page, texto, mensaje)


async def _servicio_compartir_texto_async(page, texto, titulo):
    try:
        servicio = ft.Share()
        page.services.append(servicio)
        page.update()
        await servicio.share_text(texto, title=titulo)
        return True
    except Exception:
        _snack(page, "No se pudo abrir el panel de compartir.")
        return False


def _servicio_compartir_texto(page, texto, titulo):
    return _programar(page, _servicio_compartir_texto_async, page, texto, titulo)


def _mostrar_dialogo_compartir_texto(page, texto, titulo, urls):
    def cerrar(e=None):
        dialog.open = False
        page.update()

    def abrir(url, modo):
        cerrar()
        _abrir_url(page, url, modo=modo)

    def compartir_sistema(e=None):
        cerrar()
        _servicio_compartir_texto(page, texto, titulo)

    def copiar_enlace(e=None):
        _copiar_texto(page, urls[-1], "Enlace copiado.")

    def copiar_texto(e=None):
        _copiar_texto(page, texto)

    dialog = ft.AlertDialog(
        title=ft.Text("Compartir"),
        content=ft.Text("Elija como quiere compartir este contenido."),
        actions=[
            ft.ElevatedButton(
                "WhatsApp",
                icon=ft.Icons.CHAT,
                on_click=lambda e: abrir(
                    urls[0],
                    LaunchMode.EXTERNAL_NON_BROWSER_APPLICATION,
                ),
            ),
            ft.OutlinedButton(
                "WhatsApp Web",
                on_click=lambda e: abrir(
                    urls[1],
                    LaunchMode.EXTERNAL_APPLICATION,
                ),
            ),
            ft.OutlinedButton(
                "Compartir",
                icon=ft.Icons.SHARE,
                on_click=compartir_sistema,
            ),
            ft.OutlinedButton("Copiar enlace", on_click=copiar_enlace),
            ft.TextButton("Copiar texto", on_click=copiar_texto),
            ft.TextButton("Cerrar", on_click=cerrar),
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()
    return True


def compartir_texto(page, texto, titulo="Compartir"):
    texto = str(texto)
    texto_url = quote(texto, safe="")
    urls_whatsapp = [
        f"whatsapp://send?text={texto_url}",
        f"https://api.whatsapp.com/send?text={texto_url}",
        f"https://wa.me/?text={texto_url}",
    ]

    return _mostrar_dialogo_compartir_texto(page, texto, titulo, urls_whatsapp)


def _mostrar_exportado(page, ruta, titulo="Archivo listo"):
    ruta = Path(ruta)

    def cerrar(e=None):
        dialog.open = False
        page.update()

    def abrir_archivo(e=None):
        cerrar()
        _abrir_url(page, ruta.as_uri(), LaunchMode.EXTERNAL_APPLICATION)

    def copiar(e=None):
        _copiar_texto(page, ruta, "Ruta copiada.")

    dialog = ft.AlertDialog(
        title=ft.Text(titulo),
        content=ft.Text(
            "El archivo se guardo correctamente. Si el panel de compartir no se abre en este equipo, "
            "puede abrir el archivo o copiar su ruta."
        ),
        actions=[
            ft.ElevatedButton(
                "Abrir archivo",
                icon=ft.Icons.OPEN_IN_NEW,
                on_click=abrir_archivo,
            ),
            ft.OutlinedButton(
                "Copiar ruta",
                icon=ft.Icons.CONTENT_COPY,
                on_click=copiar,
            ),
            ft.TextButton("Cerrar", on_click=cerrar),
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()
    return True


async def _compartir_archivo_async(page, archivo, titulo, mime_type):
    try:
        ruta = Path(archivo)
        servicio = ft.Share()
        page.services.append(servicio)
        page.update()
        await servicio.share_files(
            [
                ft.ShareFile(
                    path=str(ruta),
                    name=ruta.name,
                    mime_type=mime_type,
                )
            ],
            title=titulo,
            text=titulo,
            subject=titulo,
            download_fallback_enabled=True,
            mail_to_fallback_enabled=True,
        )
        return True
    except Exception:
        try:
            _mostrar_exportado(page, Path(archivo), "Archivo listo")
        except Exception:
            _snack(page, "No se pudo abrir el panel para exportar el archivo.")
        return False


def compartir_archivo(
    page,
    archivo,
    titulo="Exportar archivo",
    mime_type="application/octet-stream",
):
    _snack(page, "Abriendo panel de compartir...")
    iniciado = _programar(
        page,
        _compartir_archivo_async,
        page,
        archivo,
        titulo,
        mime_type,
    )

    if not iniciado:
        return _mostrar_exportado(page, Path(archivo), "Archivo listo")

    return True
