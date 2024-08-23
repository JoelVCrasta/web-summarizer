/* modes = ['text', 'url', 'file'];

mode = document.getElementById('mode');

mode.addEventListener('click', function() {
    
}) */

userText = document.getElementById('text'); 
urlText = document.getElementById('url');
outputText = document.getElementById('summary');
submitButton = document.getElementById('submit');

submitButton.addEventListener('click', function() {
    let text = userText.value;
    let url = urlText.value;

    axios.post(
        'http://127.0.0.1:8000/summary',
         { mode: 2, text: text, url: url, sum_len: 'long' }
    )
    .then(function(response) {
        outputText.innerHTML = response.data;
    })
    .catch(function(error) {
        console.log(error);
    });

    

});