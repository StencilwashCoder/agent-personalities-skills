import { loadStripe } from '@stripe/stripe-js';

// Make sure to call `loadStripe` outside of a component's render to avoid
// recreating the `Stripe` object on every render.
const stripePublishableKey = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || '';

export const stripePromise = stripePublishableKey 
  ? loadStripe(stripePublishableKey)
  : null;

export const STRIPE_PRICE_IDS = {
  starter: process.env.NEXT_PUBLIC_STRIPE_STARTER_PRICE_ID || 'price_starter_placeholder',
  growth: process.env.NEXT_PUBLIC_STRIPE_GROWTH_PRICE_ID || 'price_growth_placeholder',
  scale: process.env.NEXT_PUBLIC_STRIPE_SCALE_PRICE_ID || 'price_scale_placeholder',
};

export const SUBSCRIPTION_LINKS = {
  starter: process.env.NEXT_PUBLIC_STRIPE_STARTER_LINK || '#',
  growth: process.env.NEXT_PUBLIC_STRIPE_GROWTH_LINK || '#',
  scale: process.env.NEXT_PUBLIC_STRIPE_SCALE_LINK || '#',
};