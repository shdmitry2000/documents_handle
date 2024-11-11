import typer

app = typer.Typer()

@app.command()
def run_fine_tuning():
    """Runs the fine-tuning process."""
    fine_tune_module()

if __name__ == "__main__":
    app()