



document.addEventListener('DOMContentLoaded', function() {
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');
    
    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
    });
    
    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
    });
});



	$(document).ready(function(){

		var multipleCancelButton = new Choices('#choices-multiple-remove-button', {
		removeItemButton: true,
		maxItemCount:3,
		searchResultLimit:5,
		renderChoiceLimit:5
		});
	   
	   
		});
