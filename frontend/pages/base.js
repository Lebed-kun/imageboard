/**
 * 
 * @param {string} title 
 * @param {string} content 
 * @param {?Object} preloadedState
 * 
 * @returns {string} 
 */
const Page = (title, content, preloadedState) => `
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=\, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>${title}</title>
            </head>
            <body>
                ${content}
            
                ${typeof preloadedState !== 'undefined' ? `
                    <script>
                        window.__PRELOADED_STATE__ = ${JSON.stringify(preloadedState)};
                    </script>
                ` : ''}
            
                <script src="/static/js/app.js"></script>
            </body>
        </html>
    `;

export default Page;