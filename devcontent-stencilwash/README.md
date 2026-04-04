# Stencilwash Content Agency

Premium technical content for developer tools, APIs, and SaaS companies.

## 🚀 Quick Start

```bash
cd devcontent-stencilwash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
devcontent-stencilwash/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Landing page
│   ├── layout.tsx         # Root layout
│   ├── success/           # Post-checkout success page
│   └── api/checkout/      # Stripe checkout API
├── content-samples/       # 5 portfolio articles
├── lib/
│   └── stripe.ts          # Stripe configuration
├── public/                # Static assets
└── ...
```

## 💳 Stripe Setup

1. Copy `.env.local.example` to `.env.local`
2. Add your Stripe keys from https://dashboard.stripe.com
3. Create 3 subscription products in Stripe
4. Generate checkout links for each product
5. Add checkout links to `.env.local`

## 📝 Content Samples

Five production-ready technical articles:

1. **Building Real-Time APIs with WebSockets and Node.js** - Backend engineering deep dive
2. **The Complete Guide to Database Sharding** - Database architecture at scale
3. **Zero-Downtime Deployments with Kubernetes** - DevOps best practices
4. **GraphQL vs REST: A Decision Framework** - API design comparison
5. **Observability-Driven Development** - Software engineering practices

## 🎯 Pricing Tiers

| Plan | Price | Deliverables |
|------|-------|--------------|
| Starter | $499/mo | 2 posts, SEO, 48hr turnaround |
| Growth | $1,499/mo | 6 posts, unlimited revisions, strategy |
| Scale | $3,999/mo | 15 posts, dedicated writer, same-day |

## 📈 Acquisition Strategy

See `ACQUISITION_STRATEGY.md` for:
- Target customer profile
- Outreach templates (Twitter, LinkedIn)
- Sales process
- Path to $20K MRR

## 🛠️ Tech Stack

- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **Payments**: Stripe
- **Deployment**: Vercel (recommended)

## 📄 License

Private - Stencilwash Content Agency
