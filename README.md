# Reuters Scrape: Python - Minimal

This project for scraping news from the Reuters website was built using pure Python along with the Robocorp library, RPaframework, and undetected-chrome. 

The application follows the principles of [Hexagonal Architecture](https://scalastic.io/en/hexagonal-architecture/#:~:text=Hexagonal%20architecture%20is%20an%20architectural,communicate%2C%20using%20ports%20and%20adapters.) and clean code, ensuring that in the future, scraping engines can be modified without changing the business rules. 

To maintain code readability, we used Black as the code formatter along with Flake8. 

The application's goal is to scrape news from the Reuters website and store specific information in an XLSX file, based on search terms, sections, and date ranges.

## Running

#### VS Code
1. Get [Robocorp Code](https://robocorp.com/docs/developer-tools/visual-studio-code/extension-features) -extension for VS Code.
1. You'll get an easy-to-use side panel and powerful command-palette commands for running, debugging, code completion, docs, etc.

#### Command line

1. [Get RCC](https://github.com/robocorp/rcc?tab=readme-ov-file#getting-started)
1. Use the command: `rcc run`

## Results

🚀 After running the bot, check out the `log.html` under the `output` -folder.

## Dependencies

All dependencies are listed in the conda.yaml file, which serves the same purpose as a requirements.txt file

