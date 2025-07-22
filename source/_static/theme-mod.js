// Solution taken from  https://github.com/executablebooks/sphinx-book-theme/issues/394#issuecomment-2594639839
const OLD_SEARCH_DIALOG_SELECTOR_NAME = 'pst-search-dialog'; 
document.addEventListener('DOMContentLoaded', () => {
	const dialog = document.getElementById(OLD_SEARCH_DIALOG_SELECTOR_NAME);
	if (dialog) {
		dialog.remove();
	}
       const sphinxPyDataCtrlKListener = getEventListeners(window).keydown[0].listener;
       window.removeEventListener("keydown", sphinxPyDataCtrlKListener, true);
});
