const slider = document.querySelector('.slider');
const followers = document.querySelector('#followers');
const following = document.querySelector('#following');
const followersTab = document.getElementById('followers');
const followingTab = document.getElementById('following');

var sectionIndex = 0;

function setSelectedTabOnLoad() {
    const selectedTab = localStorage.getItem('selectedTab');
    if (selectedTab === 'following') {
        sectionIndex = 1;
        slider.style.transform = 'translate(' + (sectionIndex) * -50 + '%)';
        followingTab.classList.add('selected');
        followersTab.classList.remove('selected');
    } else {
        sectionIndex = 0;
        slider.style.transform = 'translate(' + (sectionIndex) * -50 + '%)';
        followersTab.classList.add('selected');
        followingTab.classList.remove('selected');
    }
}

setSelectedTabOnLoad();

followers.addEventListener('click', function() {
    if (sectionIndex !== 0) {
        sectionIndex = 0;
        slider.style.transform = 'translate(' + (sectionIndex) * -50 + '%)';
        followersTab.classList.add('selected');
        followingTab.classList.remove('selected');
        localStorage.setItem('selectedTab', 'followers');
    }
});

following.addEventListener('click', function() {
    if (sectionIndex !== 1) {
        sectionIndex = 1;
        slider.style.transform = 'translate(' + (sectionIndex) * -50 + '%)';
        followersTab.classList.remove('selected');
        followingTab.classList.add('selected');
        localStorage.setItem('selectedTab', 'following');
    }
});