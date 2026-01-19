document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('bookGrid');
    const searchInput = document.getElementById('searchInput');
    const resultCount = document.getElementById('resultCount');
    const filterBtns = document.querySelectorAll('.filter-btn');
    
    let currentFilter = 'all';
    
    // Sort logic: Higher ID means newer (Assuming sequential IDs)
    // If IDs are not sequential, we just rely on array order (last added is last in array) then reverse.
    // However, explicit sort is safer.
    libraryData.sort((a, b) => {
        const idA = parseInt(a.id) || 0;
        const idB = parseInt(b.id) || 0;
        return idB - idA; // Descending
    });

    // Initial Render
    renderBooks(libraryData);
    
    // Search Handler
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        filterAndRender(query, currentFilter);
    });
    
    // Filter Handler
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Apply filter
            currentFilter = btn.dataset.filter;
            filterAndRender(searchInput.value.toLowerCase(), currentFilter);
        });
    });
    
    function filterAndRender(query, filter) {
        let filtered = libraryData.filter(book => {
            const matchQuery = 
                book.title.toLowerCase().includes(query) || 
                book.author.toLowerCase().includes(query);
                
            const matchFilter = filter === 'all' ? true : book.category === filter;
            
            return matchQuery && matchFilter;
        });
        
        renderBooks(filtered);
    }
    
    function renderBooks(books) {
        grid.innerHTML = '';
        
        if (books.length === 0) {
            grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--text-secondary)">검색 결과가 없습니다.</div>';
            resultCount.textContent = '0 items';
            return;
        }
        
        resultCount.textContent = `${books.length} items`;
        
        books.forEach(book => {
            const card = document.createElement('div');
            card.className = 'book-card';
            
            // Fallback for link
            const linkUrl = book.link || book.source || '#';
            const linkText = (book.link || book.source) ? 'View Resource' : 'No Link Available';
            const linkClass = (book.link || book.source) ? 'book-link' : 'book-link disabled';
            const category = book.category ? book.category : 'Theology';
            
            card.innerHTML = `
                <div class="book-meta">${category}</div>
                <h3 class="book-title">${book.title}</h3>
                <div class="book-author">${book.author}</div>
                <a href="${linkUrl}" class="${linkClass}" target="_blank">
                    <span>${linkText}</span>
                    <i class="ri-arrow-right-line"></i>
                </a>
            `;
            
            grid.appendChild(card);
        });
    }
});
