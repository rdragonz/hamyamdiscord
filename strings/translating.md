# Translations Guide

Hamyambot aims to be available in as many languages as possible. As a result, the software can be translated into any language! By default, the code for Hamyambot ships with the language pack "en_US" enabled in the configuration. If you notice that your language is not available as part of Hamyambot and you want to assist in the translation efforts, please follow these guidelines:

1. The commands cannot be changed.
2. All translations should be 100% complete when a pull request is made for the added language file.
3. All translations should not modify the main README file, the main hamyambot.py file, or anything in the hamyam library folder. The software supports translations through .lang files alone.
4. The .lang file should be formatted in valid JSON format. If you're not sure if your JSON is valid, use a JSON validation tool to double-check!
5. If you are going to translate the help.txt file in the root of this folder, you **MUST** leave the attribution statements that mention who the bot was created by, the original link to this repository, and the note that this bot is licensed under GPLv3 un-translated.
6. A translated help.txt file may be included within the strings folder. Please format the file with the name "help-{LOCALIZATION CODE}.txt".

## Submitting a new language

Please use the "Pull Request" feature available on GitHub at the source of the original repository your copy of the source code was acquired from.

In the pull request, please ensure that your branch is fully up-to-date with the latest version of HamYam bot and ensure that the only modified files in the pull request are addtions of the language file and/or a corresponding help.txt file.

If you include changes that are not on the current "main" branch of the source repository, your pull request will be rejected without review.

## Fixing translation errors in existing translations

If a translation error is noticed, a pull request can be made that fixes the corresponding .lang file, or help-{LOCALIZATION CODE}.txt file. The corrected translation will be reviewed for accuracy. 
