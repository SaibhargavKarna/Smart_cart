// Toggle function for Filters
function toggleFunction(formId) {
    toggleForm = document.getElementById(formId);
    toggleForm.classList.toggle('hidden');
  }

// csrftoken
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


// Add to Cart function for products
var updateButtons=document.getElementsByClassName('update-cart')

for(var i=0; i < updateButtons.length; i++){
    updateButtons[i].addEventListener('click',function(){
        var productId=this.dataset.product
        var action=this.dataset.action
        // console.log('productId:',productId,'action:',action)
        // console.log('USER:',user)

        if(user==='AnonymousUser'){
            alert('Please Login to Continue!')
        }else{
            updateUserOrder(productId,action)
        }
    })
}

function updateUserOrder(productId,action){
    console.log('User is logged in, sending data...')

    var url='/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })

    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })
}


