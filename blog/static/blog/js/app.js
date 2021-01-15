// モーダル処理
for (const element of document.querySelectorAll('.modal-delete, .show-modal')) {
    element.addEventListener('click', e => {
        const modalId = element.dataset.target;
        const modal = document.getElementById(modalId);
        modal.classList.toggle('active');
    });
}

// コメントプレビュー
//document.querySelectorAll('.toggle-preview').forEach(el =>{
//	
//	el.addEventListener('click',(e) => {
//		el.querySelector('i').classList.toggle('fa-toggle-on');
//		el.parentNode.querySelector('.markdownx-editor').classList.toggle("active")
//		el.parentNode.querySelector('.markdownx-preview').classList.toggle("active")
//	})
//});

for (const link of document.querySelectorAll('a')){
	
	link.addEventListener('click', e => {
		
		const href = link.getAttribute('href')
		
		if (href.startsWith('#')){
			console.log(href);
			return;
		
		}else{
			e.preventDefault();
			const loader = document.querySelector('.loader-wrapper')
			loader.classList.add('loading')
			setTimeout(e => {
				location.href = href	
			},500)			
		}


	})
}

