# YouTube Commnt Scraper

This project is a Python-based tool for scraping YouTube comments using `BeautifulSoup` and `Selenium`. Follow the instructions below to set up the environment and execute the script.

# Prerequisites

Before starting, ensure that you have the following installed on your system:

1. **Conda** (Miniconda or Anaconda)
2. **Google Chrome Browser**
   - Make sure you have the latest version of Google Chrome installed. You can download it from [Google Chrome Official Site](https://www.google.com/chrome/what-you-make-of-it/).

3. **ChromeDriver**
   - Install the ChromeDriver that matches your browser version. You can find the correct driver for your version at the [Chrome for Testing Downloads](https://googlechromelabs.github.io/chrome-for-testing/), or [Chrome for developers](https://developer.chrome.com/docs/chromedriver/downloads?hl=ko).
   - Later, you should specify the absolute path to downloaded `ChromeDriver` in the `ytCommentScraper.py` file.

# Setup Instructions

## 1. Clone this Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/zoshs2/YoutubeCommentScraper.git
cd YoutubeCommentScraper 
```

## 2. Create a Conda Environment

Use the `environment.yml` file to set up the required Conda environment.

### Step 1: Create the environment

```bash
conda env create -n my_env_name -f environment.yml
```

### NOTE on pip Errors

If you encounter the following error:

```bash
CondaEnvException: Pip failed
```
This can occur if pip-related dependencies in the `environment.yml` file fail to install. However, this issue seems not affect the my script's execution in most cases. 

### Step 2: Activate the environment

```bash
conda activate my_env_name
```

# Running the Scraping Script

## 1. Update Configuration (TODO)

If your script requires any specific settings (e.g., YouTube video URL, Saving Path, Chrome Driver Path etc.), edit the `ytCommentScraper.py` file or provide necessary input when prompted.

## 2. Execute the Script

Run the script using the following command:

```bash
python ytCommentScraper.py
```

# Troubleshooting

- **Error**: `CondaValueError: The target prefix is the base prefix.`
: Make sure to deactivate the base environment before creating a new one:
```bash
conda deactivate
```

- **CondaEnvException: Pip failed**
: This error occurs during the creation of the Conda environment due to pip-related issues. In most cases, this does not affect the functionality of the script, and you can proceed with the setup and execution.

# Acknowledgments

Thanks to the open-source community for providing libraries such as `BeautifulSoup`, `Requests`, and `Selenium` for web scraping.