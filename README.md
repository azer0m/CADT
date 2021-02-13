# CADT
Canvas Auto Download Tool (CADT) allows the user to automatically download all
files and (accessible) submissions from their institution's Canvas portal. In
order to use CADT, clone this repo and follow all of the README instructions
below.

# Requirements
This tool is designed for use on a `macOS` operating system with `Python 3` and
requires `pip`.

# Input Your Credentials
First, you need to provide CADT with the proper credentials to access your
Canvas
portal: your institution's **_Canvas URL_** and an **_Access Token_**. Input
both the URL and token within `credentials.py`:
```python
CANVAS_URL = "" # YOUR INSTITUTION'S CANVAS URL GOES HERE (e.g. https://xcourses.xuniversity.edu/)
ACCESS_TOKEN = "" # YOUR CANVAS ACCESS TOKEN GOES HERE (see README for how to obtain this)
```

### Canvas URL
Your **_Canvas URL_** should be known to you already. It is usually something like: `https://xcourses.xuniversity.edu/`.

### Access Token
To obtain your **_Access Token_**, you'll need to do the following:

1. Login to your Canvas portal
2. Head to **Account** &#8594; **Settings**

    ![Account_Settings](https://github.com/azer0m/CADT/blob/main/images/Account_Settings.png?raw=true)
3. Scroll to **Approved Integrations** and click **New Access Token**
4. For **Purpose**, type `Admin API`, leave **Expires** blank, and click
   **Generate Token**

    ![Account_Settings](https://github.com/azer0m/CADT/blob/main/images/Generate_Access_Token.png?raw=true)
5. Follow the instructions and copy your **Access Token** now, otherwise you
   will lose it and have to regenerate one

   ![Account_Settings](https://github.com/azer0m/CADT/blob/main/images/Copy_Token.png?raw=true)
6. Place your full **Access Token** in `credentials.py`.

Your `credentials.py` file should now look something like this:
```python
CANVAS_URL = "https://xcourses.xuniversity.edu/" # YOUR INSTITUTION'S CANVAS URL GOES HERE (e.g. https://xcourses.xuniversity.edu/)
ACCESS_TOKEN = "alpha_numerical_key" # YOUR CANVAS ACCESS TOKEN GOES HERE (see README for how to obtain this)
```

# Running CADT
Navigate to the `CADT/` directory and execute the following command:
```bash
./cadt.sh
```

This will first install any required dependencies via `pip`, and then run the
CADT tool. Depending on how many files, submissions, and courses are associated
with the user, this may take several minutes.

All downloaded files will be placed under
`CADT/Downloaded_Files/`. See [**Caveats**](#Caveats) for what this tool can and
cannot download.

While CADT is running, the console window will print messages describing all actions taking
place. All of these messages are also placed into an `output.log` file,produced
within the `CADT/` directory.

# What Does CADT Do?
CADT uses the `canvasapi` Python [package](https://github.com/ucfopen/canvasapi) to interface with the [Canvas LMS REST
API](https://canvas.instructure.com/doc/api/). CADT iterates through every file
and submission for each course, searching for downloadable content.

# Caveats
CADT is capable of downloading course files and course submissions if they are
accessible or active. For example, courses within the **_Past Enrollments_**
category in Canvas are usually not accessible by Canvas. In these cases, special care should
be taken to download files and submission for those courses manually.