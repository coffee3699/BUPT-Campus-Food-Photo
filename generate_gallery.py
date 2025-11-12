#!/usr/bin/env python3
"""
Generate an HTML photo gallery from the Photos directory structure.
"""

import os
import json
from pathlib import Path
from urllib.parse import quote

def scan_photos(base_dir):
    """Scan the Photos directory and build a hierarchical structure."""
    photos = []
    
    for root, dirs, files in os.walk(base_dir):
        # Sort directories and files for consistent output
        dirs.sort()
        files.sort()
        
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, base_dir)
                
                # Parse the path structure
                parts = rel_path.split(os.sep)
                if len(parts) >= 3:
                    campus = parts[0]
                    dining_hall = parts[1]
                    dish = parts[2]
                    filename = parts[-1]
                    
                    photos.append({
                        'path': rel_path.replace(os.sep, '/'),
                        'campus': campus,
                        'dining_hall': dining_hall,
                        'dish': dish,
                        'filename': filename
                    })
    
    return photos

def organize_photos(photos):
    """Organize photos by campus and dining hall."""
    organized = {}
    
    for photo in photos:
        campus = photo['campus']
        dining_hall = photo['dining_hall']
        dish = photo['dish']
        
        if campus not in organized:
            organized[campus] = {}
        
        if dining_hall not in organized[campus]:
            organized[campus][dining_hall] = {}
        
        if dish not in organized[campus][dining_hall]:
            organized[campus][dining_hall][dish] = []
        
        organized[campus][dining_hall][dish].append(photo)
    
    return organized

def generate_html(organized_photos):
    """Generate the HTML page."""
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BUPT Campus Food Photo Archive</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
        }
        
        header {
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 3px solid #667eea;
        }
        
        h1 {
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.2em;
            color: #666;
            margin-bottom: 20px;
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .stat {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 10px;
            font-weight: bold;
        }
        
        .campus-section {
            margin-bottom: 50px;
        }
        
        .campus-title {
            font-size: 2em;
            color: #764ba2;
            margin-bottom: 30px;
            padding-left: 20px;
            border-left: 5px solid #764ba2;
        }
        
        .dining-hall {
            margin-bottom: 40px;
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
        }
        
        .dining-hall-title {
            font-size: 1.5em;
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .dish-section {
            margin-bottom: 30px;
        }
        
        .dish-title {
            font-size: 1.2em;
            color: #555;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .photo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .photo-item {
            position: relative;
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            background: white;
        }
        
        .photo-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        .photo-item img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            display: block;
            cursor: pointer;
        }
        
        .photo-caption {
            padding: 10px;
            font-size: 0.9em;
            color: #666;
            text-align: center;
            background: white;
        }
        
        /* Lightbox styles */
        .lightbox {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.9);
        }
        
        .lightbox.active {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .lightbox-content {
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
        }
        
        .lightbox-close {
            position: absolute;
            top: 20px;
            right: 40px;
            color: white;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.3s;
        }
        
        .lightbox-close:hover {
            color: #667eea;
        }
        
        .lightbox-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            padding: 20px;
            user-select: none;
            transition: color 0.3s;
        }
        
        .lightbox-nav:hover {
            color: #667eea;
        }
        
        .lightbox-prev {
            left: 20px;
        }
        
        .lightbox-next {
            right: 20px;
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #eee;
            color: #666;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            h1 {
                font-size: 1.8em;
            }
            
            .photo-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 10px;
            }
            
            .photo-item img {
                height: 150px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🍜 BUPT Campus Food Photo Archive</h1>
            <p class="subtitle">北京邮电大学校园美食图片档案</p>
            <div class="stats">
                <div class="stat">📸 Total Photos: {total_photos}</div>
                <div class="stat">🏫 Campuses: {campus_count}</div>
                <div class="stat">🍽️ Dining Halls: {dining_hall_count}</div>
            </div>
        </header>
        
        <main>
'''
    
    total_photos = 0
    campus_count = len(organized_photos)
    dining_hall_count = sum(len(halls) for halls in organized_photos.values())
    
    for campus in sorted(organized_photos.keys()):
        html += f'            <div class="campus-section">\n'
        html += f'                <h2 class="campus-title">{campus}</h2>\n'
        
        for dining_hall in sorted(organized_photos[campus].keys()):
            html += f'                <div class="dining-hall">\n'
            html += f'                    <h3 class="dining-hall-title">📍 {dining_hall}</h3>\n'
            
            for dish in sorted(organized_photos[campus][dining_hall].keys()):
                photos = organized_photos[campus][dining_hall][dish]
                total_photos += len(photos)
                
                html += f'                    <div class="dish-section">\n'
                html += f'                        <h4 class="dish-title">🍴 {dish}</h4>\n'
                html += f'                        <div class="photo-grid">\n'
                
                for photo in photos:
                    photo_path = quote('Photos/' + photo['path'])
                    html += f'                            <div class="photo-item">\n'
                    html += f'                                <img src="{photo_path}" alt="{photo["filename"]}" onclick="openLightbox(this.src)">\n'
                    html += f'                                <div class="photo-caption">{photo["filename"]}</div>\n'
                    html += f'                            </div>\n'
                
                html += f'                        </div>\n'
                html += f'                    </div>\n'
            
            html += f'                </div>\n'
        
        html += f'            </div>\n'
    
    html += '''        </main>
        
        <footer class="footer">
            <p>Made with ❤️ for BUPT Campus Community</p>
            <p>Special thanks to QIN SHUANG for her unwavering support</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                <a href="https://github.com/coffee3699/BUPT-Campus-Food-Photo" style="color: #667eea; text-decoration: none;">
                    View on GitHub
                </a>
            </p>
        </footer>
    </div>
    
    <!-- Lightbox -->
    <div id="lightbox" class="lightbox" onclick="closeLightbox(event)">
        <span class="lightbox-close" onclick="closeLightbox(event)">&times;</span>
        <span class="lightbox-nav lightbox-prev" onclick="navigateLightbox(-1)">&#10094;</span>
        <img id="lightbox-img" class="lightbox-content" src="" alt="">
        <span class="lightbox-nav lightbox-next" onclick="navigateLightbox(1)">&#10095;</span>
    </div>
    
    <script>
        let allImages = [];
        let currentImageIndex = 0;
        
        // Collect all images on page load
        document.addEventListener('DOMContentLoaded', function() {
            const images = document.querySelectorAll('.photo-item img');
            allImages = Array.from(images).map(img => img.src);
        });
        
        function openLightbox(src) {
            const lightbox = document.getElementById('lightbox');
            const lightboxImg = document.getElementById('lightbox-img');
            currentImageIndex = allImages.indexOf(src);
            lightboxImg.src = src;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        
        function closeLightbox(event) {
            if (event.target.id === 'lightbox' || event.target.classList.contains('lightbox-close')) {
                const lightbox = document.getElementById('lightbox');
                lightbox.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        }
        
        function navigateLightbox(direction) {
            currentImageIndex += direction;
            if (currentImageIndex < 0) {
                currentImageIndex = allImages.length - 1;
            } else if (currentImageIndex >= allImages.length) {
                currentImageIndex = 0;
            }
            const lightboxImg = document.getElementById('lightbox-img');
            lightboxImg.src = allImages[currentImageIndex];
            event.stopPropagation();
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', function(event) {
            const lightbox = document.getElementById('lightbox');
            if (lightbox.classList.contains('active')) {
                if (event.key === 'Escape') {
                    lightbox.classList.remove('active');
                    document.body.style.overflow = 'auto';
                } else if (event.key === 'ArrowLeft') {
                    navigateLightbox(-1);
                } else if (event.key === 'ArrowRight') {
                    navigateLightbox(1);
                }
            }
        });
    </script>
</body>
</html>
'''
    
    # Replace placeholders
    html = html.replace('{total_photos}', str(total_photos))
    html = html.replace('{campus_count}', str(campus_count))
    html = html.replace('{dining_hall_count}', str(dining_hall_count))
    
    return html

def main():
    """Main function to generate the gallery."""
    photos_dir = 'Photos'
    
    if not os.path.exists(photos_dir):
        print(f"Error: {photos_dir} directory not found")
        return
    
    print("Scanning photos...")
    photos = scan_photos(photos_dir)
    print(f"Found {len(photos)} photos")
    
    print("Organizing photos...")
    organized = organize_photos(photos)
    
    print("Generating HTML...")
    html = generate_html(organized)
    
    output_file = 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Gallery generated successfully: {output_file}")
    print(f"Total photos: {len(photos)}")
    print(f"Campuses: {len(organized)}")
    print(f"Dining halls: {sum(len(halls) for halls in organized.values())}")

if __name__ == '__main__':
    main()
