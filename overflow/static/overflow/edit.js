document.addEventListener('DOMContentLoaded', () => 
{
    document.querySelector('#edit-que').addEventListener('click', () => 
    {
         document.querySelector('#que-cunt').style.display = "none";
         document.querySelector('#que-form').style.display = "block";
    });

    document.querySelector('#close-que').addEventListener('click', () => 
    {
        document.querySelector('#que-form').style.display = "none";
        document.querySelector('#que-cunt').style.display = "block";
    });

    document.querySelector('#que-form').addEventListener('submit', (event) => 
    {
         event.preventDefault();
         let body = document.querySelector('#textareaQ').value;
         let id = document.querySelector('#que_id').value;

         const csrftoken = getCookie('csrftoken');

         fetch("/eSaveQue", {
            method: "POST",
            body: JSON.stringify({
                id: id,
                body: body,
            }),
            headers: { "X-CSRFToken": csrftoken },
         })
         .then((response) => {
            console.log(response);
            console.log(marked.parse(body));
            document.querySelector('#que-body-js').innerHTML = marked.parse(body);

            document.querySelector('#que-form').style.display = "none";
            document.querySelector('#que-cunt').style.display = "block";
         })
         .catch((error) => console.log(error));
         
         return false;
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
