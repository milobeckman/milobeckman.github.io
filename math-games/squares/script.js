// html elements
const questionElement = document.getElementById('question')
const userInputElement = document.getElementById('userInput')
const timerElement = document.getElementById('timer')
const playButtonElement = document.getElementById('playButton')
const bigNumberElement = document.getElementById('bigNumber')
const inputContainerElement = document.getElementById('inputContainer')
const highScoreElement = document.getElementById('highScore')
const replayButtonElement = document.getElementById('replayButton')

// game values
var currentScore = 0
var highScore = 0
let gameLength = 60
let startTime = 0
var timerUpdater

// style values
let defaultFontSize = 13
var fontSize = 13


/*****     on load, start the game!     *****/
loadPage()


// hide the game, show a 60 second timer and play button
function loadPage() {
    bigNumberElement.style.visibility = 'hidden'
    inputContainerElement.style.visibility = 'hidden'
    timerElement.innerText = 'Squares Blitz'

    playButtonElement.addEventListener('click', function(event) {startGame()})
}


// reset and start new game
function startGame() {

    // hide play button and post-game elements
    playButtonElement.style.visibility = 'hidden'
    highScoreElement.style.visibility = 'hidden'
    replayButtonElement.style.visibility = 'hidden'

    // show game elements
    bigNumberElement.style.visibility = 'visible'
    inputContainerElement.style.visibility = 'visible'
    questionElement.style.visibility = 'visible'
    userInputElement.style.visibility = 'visible'

    // clear and select user input
    userInputElement.value = ''
    userInputElement.focus()
    userInputElement.select()


    currentScore = 0
    fontSize = defaultFontSize

    updateBigNumber()
    updateQuestion()
    startTimer()
}

// update the main score visual and readjust size if necessary
function updateBigNumber() {
    bigNumberElement.innerText = answerString(currentScore)
    checkTextOverflow()
}

// update the input prompt
function updateQuestion() {
    questionElement.innerText = (currentScore + 1) + " × " + (currentScore + 1) + " = "
}

// reset the timer at the start of game, begin countdown
function startTimer() {
    startTime = new Date()
    updateTimer()
    if (timerUpdater) {
        clearInterval(timerUpdater)
    }
    timerUpdater = setInterval(updateTimer, 1000)
}

// once a second, update the timer visual
function updateTimer() {
    let timeLeft = gameLength - timeElapsed()

    var minutes = Math.floor(timeLeft / 60)
    var seconds = timeLeft % 60

    if (seconds >= 10) {
        timerElement.innerText = '' + minutes + ':' + seconds
    } else {
        timerElement.innerText = '' + minutes + ':0' + seconds
    }
    if (timeLeft == 0) {
        endGame()
    } 
}

function timeElapsed() {
    return Math.floor((new Date() - startTime) / 1000)
}

// user has successfully entered the next number, update everything
function incrementScore() {
    currentScore++
    updateBigNumber()
    updateQuestion()
    userInputElement.value = ''
}

// if bigNumber is larger than the screen width, shrink the size
function checkTextOverflow() {
    if (bigNumberElement.scrollWidth > bigNumberElement.clientWidth) {
        fontSize = fontSize * 10/13
    }

    bigNumberElement.style.fontSize = fontSize + "rem"
}

// after 60 seconds, disable number entry and show score + high score
function endGame() {
    timerElement.innerText = "Game Over"
    clearInterval(timerUpdater)
    hideInput()
    updateHighScore()
    displayHighScore()
    displayReplayButton()
}

function hideInput() {
    questionElement.style.visibility = 'hidden'
    userInputElement.style.visibility = 'hidden'
}

// compare current score to stored high score, update if necessary
function updateHighScore() {
    try {
        highScore = parseFloat(localStorage.highScoreSquares)
        if (isNaN(highScore)) {
            highScore = 0
        }
    } catch (e) {
        highScore = 0
    }

    if (currentScore > highScore) {
        highScore = currentScore
        localStorage.highScoreSquares = '' + currentScore
        timerElement.innerText = "New High Score!"
    }
}

// make the high score display visible
function displayHighScore() {
    highScoreElement.style.visibility = 'visible'
    highScoreElement.innerText = 'High Score: ' + answerString(highScore)
}

function displayReplayButton() {
    replayButtonElement.style.visibility = 'visible'
    replayButtonElement.addEventListener('click', function(event) {startGame()})
}

// the desired input to increase your score to n
function correctAnswer(n) {
    return n**2
}

function answerString(n) {
    return correctAnswer(n).toLocaleString()
}

// await user input and check if they've entered the correct number
userInputElement.addEventListener('input', () => {
    const currentInput = userInputElement.value
    if (currentInput == correctAnswer(currentScore+1)) {
        incrementScore()
    }
})

