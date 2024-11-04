# Car Web blog
I've created a web blog site about Cars

# How to change the database to PostgreSQL
after installing PostgreSQL do the steps below:

1 - go to settings.py

2 - find the database part

3 - replace the fields below with your database information

    'NAME': 'your database name',
    'USER': 'your username',
    'PASSWORD': 'username password',
    'PORT': 'your port number',
    
# notes
after running the server in the URL part add \CarBlog at the end

**To use the search feature you have to have Postgresql installed**

the database is PostgreSQL now (it was the default one before)

**Check the requirement file**


**_(for vs code users)_** If you've noticed some symbols like !, +, ? and some words like todo; these are for coloring the comments using "better comment" extension with the following configuration in the setting.json file


    "better-comments.multilineComments": true,
    "better-comments.highlightPlainText": true,
    "better-comments.tags": [
        {
            "tag": "!",
            "color": "#FF2D00",
            "strikethrough": false,
            "underline": false,
            "backgroundColor": "transparent",
            "bold": false,
            "italic": false
        },
        {
            "tag": "?",
            "color": "#f0ead6",
            "strikethrough": false,
            "underline": false,
            "backgroundColor": "transparent",
            "bold": false,
            "italic": false
        },
        {
            "tag": "//",
            "color": "#474747",
            "strikethrough": true,
            "underline": false,
            "backgroundColor": "transparent",
            "bold": false,
            "italic": false
        },
        {
            "tag": "todo",
            "color": "#FF8C00",
            "strikethrough": false,
            "underline": false,
            "backgroundColor": "transparent",
            "bold": false,
            "italic": false
        },
        {
            "tag": "*",
            "color": "#98C379",
            "strikethrough": false,
            "underline": false,
            "backgroundColor": "transparent",
            "bold": false,
            "italic": false
        },
        {
            "tag": "+",
            "color": "#7fffd4",
            "strikethrough": false,
            "underline": false,
            "backgroundColor": "transparent",
            "bold": false,
            "italic": false
        },
        {
            "tag": "$",
            "color": "#c3b091",
            "strikethrough": false,
            "underline": false,
            "backgroundColor": "transparent",
            "bold": false,
            "italic": false
        },
    ],
    "editor.inlayHints.enabled": "off",
    "workbench.colorCustomizations": {
        "editor.lineHighlightBackground": "#1073cf2d",
        "editor.lineHighlightBorder": "#9fced11f"
    },
