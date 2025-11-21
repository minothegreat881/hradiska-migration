"""
Setup script pre Next.js aplikáciu
Inicializuje Next.js projekt a vytvorí potrebnú štruktúru
"""

import os
import json
import subprocess
from pathlib import Path
import shutil

class NextJSSetup:
    def __init__(self, project_dir: str = "../nextjs-app"):
        self.project_dir = Path(project_dir).absolute()
        self.project_dir.mkdir(parents=True, exist_ok=True)

    def create_package_json(self):
        """Vytvorí package.json súbor"""
        package_json = {
            "name": "hradiska-sk",
            "version": "1.0.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint",
                "export": "next build && next export"
            },
            "dependencies": {
                "next": "14.0.4",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@next/mdx": "^14.0.4",
                "@mdx-js/loader": "^3.0.0",
                "@mdx-js/react": "^3.0.0",
                "gray-matter": "^4.0.3",
                "remark": "^15.0.1",
                "remark-html": "^16.0.1",
                "date-fns": "^3.0.0"
            },
            "devDependencies": {
                "@types/node": "^20",
                "@types/react": "^18",
                "@types/react-dom": "^18",
                "autoprefixer": "^10.4.16",
                "eslint": "^8",
                "eslint-config-next": "14.0.4",
                "postcss": "^8.4.32",
                "tailwindcss": "^3.4.0",
                "typescript": "^5"
            }
        }

        package_json_path = self.project_dir / "package.json"
        with open(package_json_path, 'w') as f:
            json.dump(package_json, f, indent=2)

        print(f"package.json vytvorený: {package_json_path}")

    def create_next_config(self):
        """Vytvorí next.config.js"""
        next_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  pageExtensions: ['js', 'jsx', 'mdx', 'ts', 'tsx'],
  images: {
    domains: ['hradiska.sk', 'www.hradiska.sk'],
    unoptimized: true,
  },
  output: 'standalone',
}

module.exports = nextConfig
"""
        config_path = self.project_dir / "next.config.js"
        with open(config_path, 'w') as f:
            f.write(next_config)

        print(f"next.config.js vytvorený: {config_path}")

    def create_tailwind_config(self):
        """Vytvorí tailwind.config.js"""
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#8B4513',
        'secondary': '#228B22',
        'accent': '#DAA520',
      },
      fontFamily: {
        'heading': ['Georgia', 'serif'],
        'body': ['Calibri', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
"""
        config_path = self.project_dir / "tailwind.config.js"
        with open(config_path, 'w') as f:
            f.write(tailwind_config)

        print(f"tailwind.config.js vytvorený: {config_path}")

    def create_postcss_config(self):
        """Vytvorí postcss.config.js"""
        postcss_config = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
        config_path = self.project_dir / "postcss.config.js"
        with open(config_path, 'w') as f:
            f.write(postcss_config)

        print(f"postcss.config.js vytvorený: {config_path}")

    def create_tsconfig(self):
        """Vytvorí tsconfig.json"""
        tsconfig = {
            "compilerOptions": {
                "target": "es5",
                "lib": ["dom", "dom.iterable", "esnext"],
                "allowJs": True,
                "skipLibCheck": True,
                "strict": True,
                "noEmit": True,
                "esModuleInterop": True,
                "module": "esnext",
                "moduleResolution": "bundler",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "jsx": "preserve",
                "incremental": True,
                "plugins": [
                    {
                        "name": "next"
                    }
                ],
                "paths": {
                    "@/*": ["./*"]
                }
            },
            "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
            "exclude": ["node_modules"]
        }

        tsconfig_path = self.project_dir / "tsconfig.json"
        with open(tsconfig_path, 'w') as f:
            json.dump(tsconfig, f, indent=2)

        print(f"tsconfig.json vytvorený: {tsconfig_path}")

    def create_app_structure(self):
        """Vytvorí základnú štruktúru app priečinka"""
        # Vytvorenie priečinkov
        dirs = [
            "app",
            "app/api",
            "app/components",
            "app/hradiska",
            "app/historia",
            "app/archeologia",
            "app/mytologia",
            "app/mapa",
            "app/kontakt",
            "public",
            "public/images",
            "styles",
            "lib",
            "content/posts"
        ]

        for dir_path in dirs:
            (self.project_dir / dir_path).mkdir(parents=True, exist_ok=True)

        # layout.tsx
        layout_content = """import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navigation from './components/Navigation'
import Footer from './components/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Slovanské Hradiská',
  description: 'Historické hradiská na území Slovenska',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="sk">
      <body className={inter.className}>
        <Navigation />
        <main className="min-h-screen">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}
"""
        with open(self.project_dir / "app" / "layout.tsx", 'w') as f:
            f.write(layout_content)

        # page.tsx (hlavná stránka)
        page_content = """'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import ArticleCard from './components/ArticleCard'

export default function HomePage() {
  const [recentPosts, setRecentPosts] = useState([])

  useEffect(() => {
    // Načítanie posledných článkov
    fetch('/api/articles?limit=6')
      .then(res => res.json())
      .then(data => setRecentPosts(data))
  }, [])

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Hero sekcia */}
      <section className="text-center py-16 bg-gradient-to-b from-amber-50 to-white rounded-lg mb-8">
        <h1 className="text-5xl font-heading font-bold text-primary mb-4">
          Slovanské Hradiská
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Objavte históriu a tajomstvá slovanských hradísk na území Slovenska.
          Archeologické nálezy, historické fakty a fascinujúce príbehy z našej minulosti.
        </p>
      </section>

      {/* Hlavné kategórie */}
      <section className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <CategoryCard
          title="Hradiská"
          description="Prehľad významných hradísk"
          href="/hradiska"
          icon="🏰"
        />
        <CategoryCard
          title="História"
          description="Historické udalosti a obdobia"
          href="/historia"
          icon="📜"
        />
        <CategoryCard
          title="Archeológia"
          description="Nálezy a vykopávky"
          href="/archeologia"
          icon="⚱️"
        />
        <CategoryCard
          title="Mytológia"
          description="Mýty a legendy"
          href="/mytologia"
          icon="🐉"
        />
      </section>

      {/* Najnovšie články */}
      <section>
        <h2 className="text-3xl font-heading font-bold text-primary mb-6">
          Najnovšie články
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {recentPosts.map((post: any) => (
            <ArticleCard key={post.slug} article={post} />
          ))}
        </div>
      </section>
    </div>
  )
}

function CategoryCard({ title, description, href, icon }: any) {
  return (
    <Link href={href}>
      <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer">
        <div className="text-4xl mb-4">{icon}</div>
        <h3 className="text-xl font-heading font-bold text-primary mb-2">{title}</h3>
        <p className="text-gray-600">{description}</p>
      </div>
    </Link>
  )
}
"""
        with open(self.project_dir / "app" / "page.tsx", 'w') as f:
            f.write(page_content)

        # globals.css
        globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --primary: #8B4513;
    --secondary: #228B22;
    --accent: #DAA520;
  }

  body {
    @apply text-gray-800;
  }

  h1, h2, h3, h4, h5, h6 {
    @apply font-heading;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary text-white px-4 py-2 rounded-lg hover:bg-opacity-90 transition-colors;
  }

  .card {
    @apply bg-white rounded-lg shadow-lg p-6;
  }
}
"""
        with open(self.project_dir / "app" / "globals.css", 'w') as f:
            f.write(globals_css)

        print("Štruktúra aplikácie vytvorená")

    def create_components(self):
        """Vytvorí základné komponenty"""
        # Navigation.tsx
        navigation_content = """'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false)

  const menuItems = [
    { title: 'Domov', href: '/' },
    { title: 'Hradiská', href: '/hradiska' },
    { title: 'História', href: '/historia' },
    { title: 'Archeológia', href: '/archeologia' },
    { title: 'Mytológia', href: '/mytologia' },
    { title: 'Mapa', href: '/mapa' },
    { title: 'Kontakt', href: '/kontakt' },
  ]

  return (
    <nav className="bg-primary text-white">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link href="/" className="text-2xl font-heading font-bold">
            Slovanské Hradiská
          </Link>

          {/* Desktop menu */}
          <div className="hidden md:flex space-x-6">
            {menuItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="hover:text-accent transition-colors"
              >
                {item.title}
              </Link>
            ))}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                d={isOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"}
              />
            </svg>
          </button>
        </div>

        {/* Mobile menu */}
        {isOpen && (
          <div className="md:hidden py-4">
            {menuItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="block py-2 hover:text-accent transition-colors"
                onClick={() => setIsOpen(false)}
              >
                {item.title}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  )
}
"""
        with open(self.project_dir / "app" / "components" / "Navigation.tsx", 'w') as f:
            f.write(navigation_content)

        # Footer.tsx
        footer_content = """export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white py-8 mt-12">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-heading font-bold mb-4">O projekte</h3>
            <p className="text-gray-300">
              Webstránka venovaná histórii a výskumu slovanských hradísk na území Slovenska.
            </p>
          </div>
          <div>
            <h3 className="text-xl font-heading font-bold mb-4">Rýchle odkazy</h3>
            <ul className="space-y-2 text-gray-300">
              <li><a href="/hradiska" className="hover:text-white">Hradiská</a></li>
              <li><a href="/historia" className="hover:text-white">História</a></li>
              <li><a href="/mapa" className="hover:text-white">Mapa</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-xl font-heading font-bold mb-4">Kontakt</h3>
            <p className="text-gray-300">
              info@hradiska.sk
            </p>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 Slovanské Hradiská. Všetky práva vyhradené.</p>
        </div>
      </div>
    </footer>
  )
}
"""
        with open(self.project_dir / "app" / "components" / "Footer.tsx", 'w') as f:
            f.write(footer_content)

        # ArticleCard.tsx
        article_card_content = """import Link from 'next/link'

interface Article {
  slug: string
  title: string
  excerpt?: string
  date?: string
  categories?: string[]
}

export default function ArticleCard({ article }: { article: Article }) {
  return (
    <Link href={`/article/${article.slug}`}>
      <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer h-full">
        <h3 className="text-xl font-heading font-bold text-primary mb-2">
          {article.title}
        </h3>
        {article.excerpt && (
          <p className="text-gray-600 mb-4 line-clamp-3">
            {article.excerpt}
          </p>
        )}
        <div className="flex justify-between items-center text-sm text-gray-500">
          {article.date && <span>{article.date}</span>}
          {article.categories && article.categories.length > 0 && (
            <span className="bg-gray-100 px-2 py-1 rounded">
              {article.categories[0]}
            </span>
          )}
        </div>
      </div>
    </Link>
  )
}
"""
        with open(self.project_dir / "app" / "components" / "ArticleCard.tsx", 'w') as f:
            f.write(article_card_content)

        print("Komponenty vytvorené")

    def create_api_routes(self):
        """Vytvorí API routes"""
        # API pre články
        articles_api = """import { NextResponse } from 'next/server'
import fs from 'fs'
import path from 'path'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const limit = parseInt(searchParams.get('limit') || '10')
  const category = searchParams.get('category')

  try {
    // Načítanie článkov z JSON súboru
    const articlesPath = path.join(process.cwd(), 'content', 'data', 'articles.json')
    const articlesData = fs.readFileSync(articlesPath, 'utf-8')
    let articles = JSON.parse(articlesData)

    // Filtrovanie podľa kategórie
    if (category) {
      articles = articles.filter((a: any) =>
        a.categories && a.categories.includes(category)
      )
    }

    // Limitovanie počtu
    articles = articles.slice(0, limit)

    return NextResponse.json(articles)
  } catch (error) {
    return NextResponse.json({ error: 'Failed to load articles' }, { status: 500 })
  }
}
"""
        api_dir = self.project_dir / "app" / "api" / "articles"
        api_dir.mkdir(parents=True, exist_ok=True)
        with open(api_dir / "route.ts", 'w') as f:
            f.write(articles_api)

        print("API routes vytvorené")

    def install_dependencies(self):
        """Nainštaluje npm dependencies"""
        print("Inštalujem npm packages...")
        try:
            subprocess.run(
                ["npm", "install"],
                cwd=self.project_dir,
                check=True,
                shell=True
            )
            print("Npm packages nainštalované úspešne")
        except subprocess.CalledProcessError as e:
            print(f"Chyba pri inštalácii npm packages: {e}")
            print("Skúste spustiť 'npm install' manuálne v priečinku nextjs-app")

def main():
    """Hlavná funkcia"""
    setup = NextJSSetup()

    print("Nastavujem Next.js projekt...")
    print("=" * 50)

    # Vytvorenie konfiguračných súborov
    setup.create_package_json()
    setup.create_next_config()
    setup.create_tailwind_config()
    setup.create_postcss_config()
    setup.create_tsconfig()

    # Vytvorenie štruktúry aplikácie
    setup.create_app_structure()
    setup.create_components()
    setup.create_api_routes()

    # Inštalácia dependencies
    setup.install_dependencies()

    print("\n" + "=" * 50)
    print("Next.js projekt je pripravený!")
    print(f"Projekt sa nachádza v: {setup.project_dir}")
    print("\nĎalšie kroky:")
    print("1. cd nextjs-app")
    print("2. npm run dev  # Spustenie vývojového servera")
    print("3. Otvorte http://localhost:3000")

if __name__ == "__main__":
    main()