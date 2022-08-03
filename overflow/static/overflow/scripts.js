document.addEventListener("DOMContentLoaded", () => 
{
  let x = document.querySelector("#upvote");

  x.addEventListener("click", () => {
    //console.log(`${x.dataset.id}downvote`);
    //get the downvote element by name and change its img src
    console.log("here");
    let y = document.getElementsByName(`${x.dataset.id}downvote`);
    y[0].src = "../static/overflow/downvote.svg";

    if(y[0].dataset.bool == "true") {
        y[0].dataset.bool = "false"
        let vote = document.querySelector(".down__vote").innerHTML;
        vote = parseInt(vote);
        vote--;
        document.querySelector(".down__vote").innerHTML = vote; 
    }
     
    const csrftoken = getCookie('csrftoken');

    if (x.dataset.bool == "true") 
    {
        x.src = "../static/overflow/upvote.svg";
        x.dataset.bool = "false";
        let vote = document.querySelector(".up__vote").innerHTML;
        vote = parseInt(vote);
        vote--;
        document.querySelector(".up__vote").innerHTML = vote;
        fetch("/unlikeUpvote", {
            method: "POST",
            body: JSON.stringify({
                id: x.dataset.id,
            }),
            headers: { "X-CSRFToken": csrftoken },
         })
         .then((response) => {
             console.log(response);
         })
         .catch((error) => console.log(error));
    }
    else{
        x.src = "../static/overflow/upvote-fill.svg";
        x.dataset.bool = "true";
        let vote = document.querySelector(".up__vote").innerHTML;
        vote = parseInt(vote);
        vote++;
        document.querySelector(".up__vote").innerHTML = vote;
        fetch("/likeUpvote", {
            method: "POST",
            body: JSON.stringify({
                id: x.dataset.id,
            }),
            headers: { "X-CSRFToken": csrftoken },
         })
         .then((response) => {
            console.log(response);
         })
         .catch((error) => console.log(error));
    }
  });

   let yy = document.querySelector('#downvote');

   yy.addEventListener('click', () => {
       
    let y = document.getElementsByName(`${x.dataset.id}upvote`);
    y[0].src = "../static/overflow/upvote.svg";
    const csrftoken = getCookie('csrftoken');
    if(y[0].dataset.bool == "true") {
        y[0].dataset.bool = "false"
        let vote = document.querySelector(".up__vote").innerHTML;
        vote = parseInt(vote);
        vote--;
        document.querySelector(".up__vote").innerHTML = vote; 
    }

    if (yy.dataset.bool == "true") 
    {
        yy.src = "../static/overflow/downvote.svg";
        yy.dataset.bool = "false";
        let vote = document.querySelector(".down__vote").innerHTML;
        vote = parseInt(vote);
        vote--;
        document.querySelector(".down__vote").innerHTML = vote;

        fetch("/dislikeDownvote", {
            method: "POST",
            body: JSON.stringify({
                id: yy.dataset.id,
            }),
            headers: { "X-CSRFToken": csrftoken },
         })
         .then((response) => {
            console.log(response);
         })
         .catch((error) => console.log(error));
    }
     else
    {
        yy.src = "../static/overflow/downvote-filled.svg";
        yy.dataset.bool = "true";
        let vote = document.querySelector(".down__vote").innerHTML;
        vote = parseInt(vote);
        vote++;
        document.querySelector(".down__vote").innerHTML = vote;

        fetch("/likeDownvote", {
            method: "POST",
            body: JSON.stringify({
                id: yy.dataset.id,
            }),
            headers: { "X-CSRFToken": csrftoken },
         })
         .then((response) => {
            console.log(response);
         })
         .catch((error) => console.log(error));
    }

   });

});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) 
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
