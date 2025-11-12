# BUPT Campus Food Photo Archive

This repository contains an organized collection of food photos from various campus dining locations. Each photo captures a specific dish, providing a visual guide for students, staff, and visitors to explore and discover the diverse food options available on campus. The photos are sorted into folders based on the location of the dining facility and further categorized into sub-folders for each individual dish.

The Campus Food Photo Archive aims to:

* Offer a comprehensive visual directory of food options available across campus dining facilities.
* Help users make informed dining choices based on their preferences and dietary needs.
* Showcase the variety and quality of food offered on campus.
* Provide a useful resource for new students, staff, and visitors to familiarize themselves with campus dining options.
* Encourage the campus community to share their own food photos and experiences, fostering a sense of community and collaboration.

## Table of Contents

- [Photo Archive Structure](#photo-archive-structure)
- [GitHub Pages Gallery](#github-pages-gallery)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

## Photo Archive Structure

The photos are organized in a hierarchical folder structure:

```
Photos/
└── 沙河校区/ (Campus Name)
    ├── 教工餐厅一层/ (Dining Hall Name)
    │   ├── 螺蛳粉/ (Dish Name)
    │   │   └── JG1-螺蛳粉.jpg (Photo)
    │   └── 烤冷面/
    │       └── JG1-烤冷面.jpg
    ├── 教工餐厅二层/
    ├── 风味餐厅一层/
    ├── 外卖/
    └── 校外美食/
```

**Structure Details:**
- **Level 1 (Campus)**: Campus location (e.g., 沙河校区)
- **Level 2 (Dining Hall)**: Specific dining facility or category (e.g., 教工餐厅一层, 风味餐厅二层, 外卖, 校外美食)
- **Level 3 (Dish)**: Individual dish or food item (e.g., 螺蛳粉, 烤冷面)
- **Level 4 (Photos)**: Actual photo files with naming convention: `[Location Code]-[Dish Name].jpg`

**Current Statistics:**
- 📸 Total Photos: 304
- 🏫 Campuses: 1 (沙河校区)
- 🍽️ Dining Halls: 15

## GitHub Pages Gallery

This repository includes an interactive web gallery accessible at: **[View Gallery](https://coffee3699.github.io/BUPT-Campus-Food-Photo/)**

### Gallery Features

The static photo gallery (`index.html`) provides:

- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **🖼️ Interactive Lightbox**: Click any photo to view full-size with navigation controls
- **⌨️ Keyboard Navigation**: Use arrow keys (←/→) to browse photos, ESC to close lightbox
- **🔍 Organized Display**: Photos grouped by Campus → Dining Hall → Dish hierarchy
- **📊 Statistics**: Real-time counts of photos, campuses, and dining halls
- **🎨 Modern UI**: Beautiful gradient theme with smooth animations

### Usage

**Viewing the Gallery:**
1. Visit the live site: [https://coffee3699.github.io/BUPT-Campus-Food-Photo/](https://coffee3699.github.io/BUPT-Campus-Food-Photo/)
2. Browse photos organized by location and dish
3. Click any photo to open the lightbox viewer
4. Use arrow keys or navigation buttons to browse through photos

**Regenerating the Gallery:**

If you add new photos to the repository, regenerate the gallery:

```bash
# Run the generator script
python3 generate_gallery.py
```

This will scan the `Photos/` directory and update `index.html` with all current photos.

**Enabling GitHub Pages** (for repository owners):
1. Go to repository **Settings** → **Pages**
2. Under "Source", select **Deploy from a branch**
3. Choose your branch (e.g., `main`) and **/ (root)** folder
4. Click **Save**
5. The site will be live at `https://[username].github.io/[repository-name]/`

### Technical Details

- **Static Site**: Pure HTML/CSS/JavaScript, no server required
- **Photo Loading**: Images are loaded directly from the repository via relative paths
- **Mobile-First**: Responsive grid layout adapts to screen size
- **Performance**: Lazy-loading principles with optimized rendering

## Getting Started

**Option 1: Browse Online**
- Visit the [GitHub Pages Gallery](https://coffee3699.github.io/BUPT-Campus-Food-Photo/) to explore photos in your browser

**Option 2: Clone Locally**
- Clone the repository or download the zip file to browse the organized folders locally:
```bash
git clone https://github.com/coffee3699/BUPT-Campus-Food-Photo.git
cd BUPT-Campus-Food-Photo
```

## Contributing

We welcome contributions to the Campus Food Photo Archive! If you have photos of campus food that you'd like to add, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Add your photos to the appropriate folders or create new folders as needed. Ensure that your photos follow the naming convention used in the repository.
4. Commit your changes and create a pull request.

We'll review your pull request and, if everything looks good, merge your changes into the main repository.

## Credits 

Special thanks is given to my lovely girlfriend QIN SHUANG, it is her unwavering support that constantly make this project a better one.

## License

This project is licensed under the [MIT License](https://en.wikipedia.org/wiki/MIT_License). See the LICENSE file for details.
