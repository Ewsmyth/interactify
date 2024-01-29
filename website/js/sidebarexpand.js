function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var contentContainer = document.querySelector('.content-container');

    sidebar.classList.toggle('expanded');
    contentContainer.classList.toggle('expanded');
}