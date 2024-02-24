# Last.fm remove scrobbles from user library where play_count = 1
For now this script creates a URL for removal of every existing artist in your last.fm with 1 play_count for cleanup purposes.

## 1 Installation (chrome configuration)

### 1-1 install tampermonkey on chrome
https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo?hl=en

### 1-2 create user script w/ the following:
```shell
(function() {
    var aa = document.querySelectorAll("input[type=checkbox]");
    for (var i = 0; i < aa.length; i++){
        aa[i].checked = true;
    }
    setTimeout(() => {
        document.forms[3].submit();
    }, "1000");
})();
```

PS. must change the `@match` tag URL to:

`@match        https://www.last.fm/user/<YOUR_LASTFM_USER>/library/music/**/+delete`

### 1-3 open last.fm on chrome and log-in with your user account

## 2 Installation (python)

```shell
pip install -r requirements.txt
```

## 3 Usage

### 3-1 Get a new dev API account on last.fm

https://www.last.fm/api/account/create

PS. You just need to enter your contact email and the application name fields.

### 3-2 Open the `config.py` file and set the values for `key`, `secret` and `username`

### 3-3 Run the script

```shell
# the script will prompt for your account password
python3 cleanup.py
```

The script will generate 2 urls for each occurrence found.
Click on the URL ending with `/+delete` to perform the auto-removal.
voilá!

## 4 Tips

You can customize the play count requirements. It is possible to increase from `1` to `5` for example.