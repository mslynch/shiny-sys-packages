import asyncio

from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.output_text_verbatim("txt"),
)

def server(input, output, session):
    @render.text
    async def txt():
        proc = await asyncio.create_subprocess_exec(
            "apt", "list", "--installed", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        return_code = await proc.wait()
        stdout, stderr = await proc.communicate()
        if return_code != 0:
            return (f"Error running command.\n"
                    f"====STDOUT====\n"
                    f"{stdout.decode()}\n"
                    f"====STDERR====\n"
                    f"{stderr.decode()}")
        return stdout


app = App(app_ui, server)
