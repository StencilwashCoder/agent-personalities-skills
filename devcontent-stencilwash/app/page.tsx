'use client'

'use client'

import { 
  PenTool, 
  Zap, 
  TrendingUp, 
  Check, 
  ArrowRight,
  FileText,
  Code,
  BookOpen,
  Sparkles
} from 'lucide-react'

import { SUBSCRIPTION_LINKS } from '@/lib/stripe'

const pricingPlans = [
  {
    name: 'Starter',
    price: '$499',
    period: '/month',
    description: 'Perfect for early-stage startups testing content marketing',
    features: [
      '2 technical blog posts/month',
      'SEO optimization included',
      '1 revision round per piece',
      '48-hour turnaround',
      'Basic analytics report',
    ],
    cta: 'Get Started',
    popular: false,
    stripeLink: SUBSCRIPTION_LINKS.starter
  },
  {
    name: 'Growth',
    price: '$1,499',
    period: '/month',
    description: 'For companies ready to scale their content engine',
    features: [
      '6 technical blog posts/month',
      'SEO + technical optimization',
      'Unlimited revisions',
      '24-hour priority turnaround',
      'Weekly analytics dashboard',
      'Social media snippets',
      'Content strategy session',
    ],
    cta: 'Start Growing',
    popular: true,
    stripeLink: SUBSCRIPTION_LINKS.growth
  },
  {
    name: 'Scale',
    price: '$3,999',
    period: '/month',
    description: 'Full content department for serious scale-ups',
    features: [
      '15 technical blog posts/month',
      'Everything in Growth',
      'Same-day delivery available',
      'Dedicated writer',
      'Custom illustrations',
      'Video script writing',
      'Monthly strategy calls',
      'White-label options',
    ],
    cta: 'Go Scale',
    popular: false,
    stripeLink: SUBSCRIPTION_LINKS.scale
  }
]

const portfolioSamples = [
  {
    title: 'Building Real-Time APIs with WebSockets and Node.js',
    category: 'Backend Engineering',
    excerpt: 'A deep dive into scaling WebSocket connections for millions of concurrent users.',
    readTime: '8 min read',
    icon: Code
  },
  {
    title: 'The Complete Guide to Database Sharding',
    category: 'Database Architecture',
    excerpt: 'How we reduced query latency by 400% through strategic data partitioning.',
    readTime: '12 min read',
    icon: DatabaseIcon
  },
  {
    title: 'Zero-Downtime Deployments with Kubernetes',
    category: 'DevOps',
    excerpt: 'Production-tested strategies for deploying without waking up the on-call engineer.',
    readTime: '10 min read',
    icon: Zap
  },
  {
    title: 'GraphQL vs REST: A Decision Framework',
    category: 'API Design',
    excerpt: 'When to choose what—and how to migrate without breaking everything.',
    readTime: '7 min read',
    icon: FileText
  },
  {
    title: 'Observability-Driven Development',
    category: 'Software Engineering',
    excerpt: 'Moving from "it works on my machine" to "we know exactly what broke."',
    readTime: '9 min read',
    icon: TrendingUp
  }
]

function DatabaseIcon(props: any) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <ellipse cx="12" cy="5" rx="9" ry="3"/>
      <path d="M3 5V19A9 3 0 0 0 21 19V5"/>
      <path d="M3 12A9 3 0 0 0 21 12"/>
    </svg>
  )
}

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-hero">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass-card border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <PenTool className="w-6 h-6 text-primary-500" />
              <span className="font-bold text-xl">Stencilwash</span>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <a href="#portfolio" className="text-gray-300 hover:text-white transition">Portfolio</a>
              <a href="#pricing" className="text-gray-300 hover:text-white transition">Pricing</a>
              <a href="#process" className="text-gray-300 hover:text-white transition">Process</a>
              <a 
                href="#pricing" 
                className="bg-primary-600 hover:bg-primary-700 px-4 py-2 rounded-lg font-medium transition"
              >
                Get Started
              </a>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-8">
            <Sparkles className="w-4 h-4 text-primary-500" />
            <span className="text-sm text-gray-300">Technical content that actually converts</span>
          </div>
          
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
            Content for developers,
            <br />
            <span className="text-gradient">written by developers</span>
          </h1>
          
          <p className="text-xl text-gray-400 max-w-2xl mx-auto mb-10">
            Premium technical content for API companies, dev tools, and SaaS platforms. 
            No fluff. No bullshit. Just code that ranks and content that converts.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="#pricing"
              className="inline-flex items-center justify-center gap-2 bg-primary-600 hover:bg-primary-700 px-8 py-4 rounded-xl font-semibold text-lg transition"
            >
              View Pricing
              <ArrowRight className="w-5 h-5" />
            </a>
            <a 
              href="#portfolio"
              className="inline-flex items-center justify-center gap-2 glass-card hover:bg-white/10 px-8 py-4 rounded-xl font-semibold text-lg transition"
            >
              See Portfolio
            </a>
          </div>
          
          <div className="mt-16 flex items-center justify-center gap-8 text-gray-500">
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-green-500" />
              <span>SEO Optimized</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-green-500" />
              <span>Technical Accuracy</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-green-500" />
              <span>48hr Turnaround</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Why teams choose Stencilwash</h2>
            <p className="text-gray-400 text-lg">Technical content that hits different</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Code,
                title: 'Actually Technical',
                description: 'Written by engineers who understand your stack. No surface-level BS.'
              },
              {
                icon: Zap,
                title: 'Fast Turnaround',
                description: '48-hour delivery standard. Same-day available on Scale plans.'
              },
              {
                icon: TrendingUp,
                title: 'Built to Rank',
                description: 'SEO-optimized from day one. Technical accuracy + search visibility.'
              }
            ].map((feature, i) => (
              <div key={i} className="glass-card p-8 rounded-2xl hover:bg-white/5 transition">
                <feature.icon className="w-10 h-10 text-primary-500 mb-4" />
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Portfolio Section */}
      <section id="portfolio" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Sample Work</h2>
            <p className="text-gray-400 text-lg">Recent technical content we've produced</p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {portfolioSamples.map((sample, i) => (
              <div key={i} className="glass-card p-6 rounded-2xl hover:bg-white/5 transition group cursor-pointer">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-3 rounded-lg bg-primary-500/10">
                    <sample.icon className="w-6 h-6 text-primary-500" />
                  </div>
                  <span className="text-sm text-primary-500 font-medium">{sample.category}</span>
                </div>
                <h3 className="text-lg font-semibold mb-2 group-hover:text-primary-500 transition">{sample.title}</h3>
                <p className="text-gray-400 text-sm mb-4">{sample.excerpt}</p>
                <div className="flex items-center text-sm text-gray-500">
                  <BookOpen className="w-4 h-4 mr-1" />
                  {sample.readTime}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">Simple, transparent pricing</h2>
            <p className="text-gray-400 text-lg">Choose a plan that fits your content needs</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {pricingPlans.map((plan, i) => (
              <div 
                key={i} 
                className={`relative glass-card p-8 rounded-2xl ${
                  plan.popular ? 'border-primary-500/50 ring-1 ring-primary-500/50' : ''
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                    <span className="bg-primary-600 text-white text-sm font-medium px-4 py-1 rounded-full">
                      Most Popular
                    </span>
                  </div>
                )}
                
                <h3 className="text-xl font-semibold mb-2">{plan.name}</h3>
                <p className="text-gray-400 text-sm mb-6">{plan.description}</p>
                
                <div className="mb-6">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  <span className="text-gray-400">{plan.period}</span>
                </div>
                
                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, j) => (
                    <li key={j} className="flex items-start gap-3">
                      <Check className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-300 text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
                
                <a
                  href={plan.stripeLink}
                  className={`block text-center py-3 rounded-xl font-semibold transition ${
                    plan.popular 
                      ? 'bg-primary-600 hover:bg-primary-700' 
                      : 'glass-card hover:bg-white/10'
                  }`}
                >
                  {plan.cta}
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section id="process" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">How it works</h2>
            <p className="text-gray-400 text-lg">Dead simple process. No meetings required.</p>
          </div>
          
          <div className="space-y-8">
            {[
              {
                step: '01',
                title: 'Subscribe',
                description: 'Pick a plan and subscribe. No sales calls. No contracts.'
              },
              {
                step: '02',
                title: 'Submit Requests',
                description: 'Send us your topic ideas via our simple form or Slack.'
              },
              {
                step: '03',
                title: 'Review Drafts',
                description: 'Get drafts within 48 hours. Request revisions if needed.'
              },
              {
                step: '04',
                title: 'Publish & Rank',
                description: 'Publish the content and watch your organic traffic grow.'
              }
            ].map((item, i) => (
              <div key={i} className="flex gap-6">
                <div className="flex-shrink-0 w-16 h-16 rounded-2xl bg-primary-500/10 flex items-center justify-center">
                  <span className="text-2xl font-bold text-primary-500">{item.step}</span>
                </div>
                <div className="pt-2">
                  <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                  <p className="text-gray-400">{item.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center glass-card p-12 rounded-3xl">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">Ready to ship better content?</h2>
          <p className="text-gray-400 text-lg mb-8">
            Join companies using Stencilwash to fuel their technical content engine.
          </p>
          <a 
            href="#pricing"
            className="inline-flex items-center gap-2 bg-primary-600 hover:bg-primary-700 px-8 py-4 rounded-xl font-semibold text-lg transition"
          >
            Get Started Today
            <ArrowRight className="w-5 h-5" />
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 sm:px-6 lg:px-8 border-t border-white/10">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-2">
              <PenTool className="w-5 h-5 text-primary-500" />
              <span className="font-semibold">Stencilwash</span>
            </div>
            
            <div className="flex items-center gap-6 text-gray-400">
              <a href="mailto:hello@stencilwash.com" className="hover:text-white transition">Contact</a>
              <a href="#" className="hover:text-white transition">Privacy</a>
              <a href="#" className="hover:text-white transition">Terms</a>
            </div>
            
            <p className="text-gray-500 text-sm">© 2026 Stencilwash. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </main>
  )
}