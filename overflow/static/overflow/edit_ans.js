document.addEventListener('DOMContentLoaded', () => 
{
    //edit button for answer
    document.querySelectorAll('#ans-edit-btn').forEach((x) => {
        x.addEventListener('click', () => {
             console.log("here")
             console.log(x.value);
             document.querySelector(`#anseditform${x.value}`).style.display = "block";
             document.querySelector(`#ansele${x.value}`).style.display = "none";
        });
    });

    //close button for ans edit
    document.querySelectorAll('#close-ans-e').forEach((x) => {
        x.addEventListener('click', () => {
            document.querySelector(`#ansele${x.value}`).style.display = "block";
            document.querySelector(`#anseditform${x.value}`).style.display = "none";
        });
    });

    //save button for ans edit
    document.querySelectorAll('.ans-edit-form').forEach((x) => 
    {
        x.addEventListener('submit', (event) => {
              event.preventDefault()
              const id = x.name;
              const body = document.querySelector(`#ta-ans-form${id}`).value;
              
              const csrftoken = getCookie('csrftoken');

              fetch("/saveAns", {
                method: "POST",
                body: JSON.stringify({
                    id: id,
                    body: body,
                }),
                headers: { "X-CSRFToken": csrftoken },
              })
              .then((response) => {
                 console.log(response);
                 document.querySelector(`#ansele${id}`).style.display = "block";
                 document.querySelector(`#anseditform${id}`).style.display = "none";
                 document.querySelector(`#sanedo${id}`).innerHTML = marked.parse(body);
              })
              .catch((error) => console.log(error));


        })
    })

    //delete button for answer
    document.querySelectorAll('#delete-ans').forEach((x) => 
    {
        x.addEventListener('click', () => 
        {
            const csrftoken = getCookie('csrftoken');
            fetch("/deleteAns", 
            {
                method: "POST",
                body: JSON.stringify({
                    id: x.value,
                }),
                headers: { "X-CSRFToken": csrftoken },
            })
            .then((response) => {
                 console.log(response);
                 document.querySelector(`#answer_elements${x.value}`).style.display = "none";
                 let val = parseInt(document.getElementById('no_answers').innerHTML);
                 val--;
                 document.getElementById('no_answers').innerHTML = val;  
            })
            .catch((error) => console.log(error));
        });
    });


})

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
