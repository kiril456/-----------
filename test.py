import flet as ft

# Define the main function
async def main(page: ft.Page):
    # Create an audio object
    audio = ft.Audio(
        src="app\songs\music\music1.mp3",
        autoplay=False,
        volume=1,
        balance=0
    )

    # Function to handle slider changes
    def slider_changed(e):
        # Calculate the new position based on the slider value
        new_position = int(e.control.value * audio.duration)
        # Set the new position of the audio track
        audio.position = new_position
        # Update the page
        page.update()

    # Add a text label
    page.add(ft.Text("Audio Player"))

    # Add the audio player and slider
    page.add(audio)
    page.add(ft.Slider(min=0, max=1, on_change=slider_changed))

    # Update the page
    await page.update_async()

# Run the Flet app
ft.app(target=main)