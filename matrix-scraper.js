const { chromium } = require('playwright');

async function scrapeMatrixMLS() {
    console.log('🚀 Starting Matrix MLS scraper...');
    
    const browser = await chromium.launch({ 
        headless: false,  // You'll see the browser
        slowMo: 1000     // Slow down for Matrix's security
    });
    
    const page = await browser.newPage();
    
    try {
        // Go to Matrix login
        console.log('📍 Going to Matrix login...');
        await page.goto('https://matrix.southfloridamls.com/Matrix/Default.aspx');
        
        // Wait for login form to load
        await page.waitForSelector('#Username', { timeout: 10000 });
        
        console.log('🔑 Enter your credentials manually for now...');
        console.log('⏰ You have 30 seconds to log in...');
        
        // Wait 30 seconds for you to manually log in
        await page.waitForTimeout(30000);
        
        // After login, navigate to search
        console.log('🔍 Looking for search options...');
        
        // Wait for you to manually navigate to search
        console.log('📋 Navigate to your property search manually...');
        console.log('⏰ You have 20 seconds...');
        await page.waitForTimeout(20000);
        
        // Try to extract property data from results
        console.log('📊 Extracting property data...');
        
        const properties = await page.evaluate(() => {
            const rows = document.querySelectorAll('tr[class*="SearchResult"]');
            const data = [];
            
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length > 0) {
                    data.push({
                        mlsNumber: cells[0]?.textContent?.trim() || '',
                        address: cells[1]?.textContent?.trim() || '',
                        price: cells[2]?.textContent?.trim() || '',
                        beds: cells[3]?.textContent?.trim() || '',
                        baths: cells[4]?.textContent?.trim() || '',
                        sqft: cells[5]?.textContent?.trim() || ''
                    });
                }
            });
            
            return data;
        });
        
        console.log(`✅ Found ${properties.length} properties!`);
        console.log('Sample data:', properties.slice(0, 3));
        
    } catch (error) {
        console.error('❌ Error:', error);
    } finally {
        console.log('🏁 Keeping browser open for 30 seconds...');
        await page.waitForTimeout(30000);
        await browser.close();
    }
}

// Run the scraper
scrapeMatrixMLS();
