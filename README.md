![hero](public/image.png)

> setached fork of https://github.com/educlopez/polaris

<p align="center">
	<h1 align="center"><b>Polaris</b></h1>
<p align="center">
    A modern, responsive personal portfolio template built with <a href="https://astro.build">Astro 7</a>.
    <br />
    <br />
    <a href="https://github.com/educlopez/Polaris/actions/workflows/ci.yml"><img src="https://github.com/educlopez/Polaris/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
    <br />
    <br />
    <a href="#whats-included"><strong>What's included</strong></a> ·
    <a href="#prerequisites"><strong>Prerequisites</strong></a> ·
    <a href="#getting-started"><strong>Getting Started</strong></a> ·
    <a href="#how-to-use"><strong>How to use</strong></a> ·
    <a href="#customization"><strong>Customization</strong></a>
  </p>
</p>

Everything you need to build a stunning personal portfolio website. Polaris is an opinionated Astro template designed for designers and developers who want to showcase their work with a clean, modern aesthetic. Built with performance and user experience in mind, it provides a solid foundation that grows with your career.

## What's included

[Astro 7](https://astro.build/) - Static site generator (Vite 8 / Rolldown, Rust compiler, Sätteri markdown)<br>
[React](https://reactjs.org/) - Interactive components<br>
[Tailwind CSS](https://tailwindcss.com/) - Utility-first styling<br>
[Lucide](https://lucide.dev/) - Beautiful icon library<br>
[TypeScript](https://www.typescriptlang.org/) - Type safety<br>
[MDX](https://mdxjs.com/) - Enhanced markdown for content<br>
[Sharp](https://sharp.pixelplumbing.com/) - Image optimization<br>
[Class Variance Authority](https://cva.style/) - Component variant management<br>
[Radix UI](https://www.radix-ui.com/) - Accessible component primitives<br>
[Biome](https://biomejs.dev/) - Fast linter & formatter<br>

## Directory Structure

```
.
├── public/                    # Static assets
│   ├── favicon.svg           # Site favicon
│   └── image.png             # Hero image
├── src/
│   ├── components/           # Reusable components
│   │   ├── ui/              # UI components (buttons, dropdowns, etc.)
│   │   ├── fade.astro       # Fade animation component
│   │   └── listProjects.astro # Project listing component
│   ├── config/
│   │   └── site.json        # Site configuration and content
│   ├── content/
│   │   └── projects/        # Project markdown files and images
│   ├── layouts/
│   │   └── Layout.astro     # Main layout component
│   ├── lib/
│   │   └── utils.ts         # Utility functions
│   ├── pages/
│   │   ├── index.astro      # Homepage
│   │   └── projects/        # Dynamic project pages
│   └── styles/
│       └── global.css       # Global styles
├── astro.config.mjs         # Astro configuration
├── components.json          # UI components configuration
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
└── vercel.json              # Vercel deployment configuration
```

## Prerequisites

Node.js (version 22.12 or higher — required by Astro 7)<br>
pnpm (recommended)<br>
Git<br>

## Customization

### Site Configuration

Update `src/config/site.json` to modify:

- Personal information and bio
- Contact details and social links
- Professional experience timeline
- Project grid layout preferences
- Company information and specialties

### Adding Projects

1. Create a new markdown file in `src/content/projects/`
2. Add project images to `src/content/projects/images/`
3. Use the existing project structure as a template with frontmatter for metadata

### Styling

- Global styles are in `src/styles/global.css`
- Component-specific styles use Tailwind CSS classes
- Smooth transitions and interactions built with CSS
- UI components follow a consistent design system

## Recognition

Built with ❤️ by [Eduardo Calvo](https://github.com/educlopez) - UI Designer & Frontend Developer based in Madrid, Spain.

Modified by Birnadin Erick.
