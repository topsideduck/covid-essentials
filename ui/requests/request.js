const request = new XMLHttpRequest();
let sendMessageRequest = (message) => {
    request.open("GET", "chat?message="+message);
    request.send();
} 