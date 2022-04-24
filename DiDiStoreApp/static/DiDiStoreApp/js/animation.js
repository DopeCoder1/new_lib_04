
let search_line = document.querySelector('.search_line');
let search_icon = document.getElementById('search_icon');
let search_form = document.querySelector('.search_form');
search_icon.addEventListener('click', ()=>{
    search_line.classList.toggle('search_line_open');
    search_form.classList.toggle('search_form_animation');
});


const showHideWindows = (show_prop, hide_prop, classList_prop, toggler_prop)=>{

    show_prop.addEventListener('click', ()=>{
        classList_prop.classList.toggle(toggler_prop);
    });
    hide_prop.addEventListener('click', ()=>{
        classList_prop.classList.toggle(toggler_prop);
    });
}

let category_window = document.querySelector('.category_window');
let hide_categories = document.getElementById('hide_categories');
let show_categories = document.getElementById('show_categories');
showHideWindows(show_categories,hide_categories,category_window,'show_window');

let registration_window = document.querySelector('.registration_window');
let hide_registrations = document.getElementById('hide_registrations');
let show_registrations = document.getElementById('show_registrations');
showHideWindows(show_registrations,hide_registrations,registration_window,'show_window');


let sign_up = document.querySelector('.sign_up');
let sign_in = document.querySelector('.sign_in');


let sign_up_btn = document.getElementById('#sign_up').addEventListener('click',()=>{
    registration_window.classList.remove('registration_window_sign_in')
    sign_in.style.display = 'none';
    sign_up.style.display = 'block';
});
let sign_in_btn = document.getElementById('#sign_in').addEventListener('click',()=>{
    registration_window.classList.add('registration_window_sign_in')
    sign_in.style.display = 'block';
    sign_up.style.display = 'none';
});


let book_modal_window = document.querySelector('.book_modal_window');
let show_modal_window = document.querySelectorAll('.buy_btn');
show_modal_window.forEach( (e) => {e.addEventListener('click',() => {
        book_modal_window.classList.toggle('show_window')
    });
});
let hide_modal_window = document.getElementById('hide_modal_window');
hide_modal_window.addEventListener('click', ()=>{
    book_modal_window.classList.toggle('show_window')
});
