import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Stencilwash Content Agency | Technical Content That Converts',
  description: 'Premium technical content for developer tools, APIs, and SaaS companies. Blog posts, documentation, and tutorials that actually convert.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}