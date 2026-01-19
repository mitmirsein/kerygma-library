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
            
            // Check content availability
            const hasContent = !!book.contentPath;
            const category = book.category ? book.category : 'Theology';
            
            // If content exists, make card clickable
            if (hasContent) {
                card.style.cursor = 'pointer';
                card.onclick = (e) => {
                    // Don't trigger if user clicked the external link button
                    if (e.target.closest('a')) return;
                    window.location.href = `article.html?id=${book.id}`;
                };
            }
            
            // External Link Logic
            const linkUrl = book.link || book.source || '#';
            const linkText = book.link ? 'Yes24/Info' : (book.source ? 'Source Link' : 'No Link');
            const showLink = (book.link || book.source);
            
            // Badge for full text
            const badgeHtml = hasContent 
                ? `<span style="background:var(--gold-primary); color:var(--bg-dark); padding:2px 6px; border-radius:4px; font-size:0.7em; font-weight:bold; margin-left:auto;"><i class="ri-article-line"></i> Full Text</span>` 
                : '';

            card.innerHTML = `
                <div class="book-meta" style="display:flex; align-items:center;">
                    <span>${category}</span>
                    ${badgeHtml}
                </div>
                <h3 class="book-title">${book.title}</h3>
                <div class="book-author">${book.author}</div>
                
                <div style="margin-top:auto; display:flex; gap:10px;">
                    ${hasContent ? `
                        <button class="book-link" style="background:transparent; border:1px solid var(--text-secondary); flex:1;" onclick="location.href='article.html?id=${book.id}'">
                            <span>Read Now</span>
                        </button>
                    ` : ''}
                    
                    ${showLink ? `
                        <a href="${linkUrl}" class="book-link" target="_blank" style="flex:1; text-align:center;">
                            <span>Link</span> <i class="ri-external-link-line"></i>
                        </a>
                    ` : ''}
                </div>
            `;
            
            grid.appendChild(card);
        });
    }
});
