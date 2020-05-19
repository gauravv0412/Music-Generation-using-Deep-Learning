# Music-Generation-using-Deep-Learning
In this project I trained my **Deep Learning Sequence Model** which consists of many **LSTM, Dense and Dropout** layers on piano instrumental music data which was available in **MIDI format**. 

In this format we have details of **notes**(a keystroke), **chords**(combination of keys) and their **offset**(time when a key(s) is pressed). We use this information to train model to predict that given these combination of notes and chords what should be played next. 

The model has recognised **600 different chords and notes** (on different octaves), and using them has produced great results.

## Installation Documentation

Step - 1: Install git on your desktop(for Mac donwload from [here](https://sourceforge.net/projects/git-osx-installer/files/) , for Windows donwload from [here](https://git-for-windows.github.io/) , for Linux run this command - `sudo apt-get install git`) and after installing verify the installation and clone this repository.

    git --version
    git clone https://github.com/gauravv0412/Music-Generation-using-Deep-Learning.git
    
![Alt text](/Screenshots/1.png)
    
Step - 2: Create virtual environment and install all the required libraries from requirements.txt. Use apt-get in case of linux and [homebrew](https://brew.sh) (`brew install`) in case of windows and linux. Refer to this [site](https://brew.sh) for Homebrew installation. Install Pyhton version == 3.7.1
  
    cd Music-Generation-using-Deep-Learning/
    
    sudo apt-get install python3.7
    sudo apt-get install python3-pip
    
![Alt text](/Screenshots/2.png)
    
    pip3 install virtualenv
    virtualenv env
    
![Alt text](/Screenshots/3.png)
    
    source env/bin/activate
    pip3 install -r requirements.txt
    
![Alt text](/Screenshots/4.png)

Step - 3: Launch Django app by: 

    python3 manage.py migrate
    python3 manage.py runserver
    
![Alt text](/Screenshots/5.png)
![Alt text](/Screenshots/6.png)

## Demo of Application

Click on **Generate Music** button and machine will start generating music. It will take around a minute to make music and MIDI file will automatically be downloaded once generation of music is complete. 

**Note: Do not press on "Generate Music" button repeatedly. Wait once it has generated music and page is reloaded. And 
        then try again generating music.**

** Preferred Browser : Google Chrome** But other will also work.

![Alt text](/Screenshots/7.png)
