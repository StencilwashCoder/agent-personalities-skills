import Link from 'next/link';

export default function SuccessPage() {
  return (
    <main className="min-h-screen bg-gradient-hero flex items-center justify-center px-4">
      <div className="glass-card p-12 rounded-3xl max-w-lg w-full text-center">
        <div className="w-20 h-20 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg 
            className="w-10 h-10 text-green-500" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M5 13l4 4L19 7" 
            />
          </svg>
        </div>
        
        <h1 className="text-3xl font-bold mb-4">Welcome to Stencilwash!</h1>
        
        <p className="text-gray-400 mb-8">
          Your subscription is confirmed. Check your email for next steps 
          and access to our content request portal.
        </p>
        
        <div className="space-y-4">
          <a 
            href="mailto:hello@stencilwash.com?subject=Content Request - Getting Started"
            className="block w-full bg-primary-600 hover:bg-primary-700 py-3 rounded-xl font-semibold transition"
          >
            Submit Your First Content Request
          </a>
          
          <Link 
            href="/"
            className="block w-full glass-card hover:bg-white/10 py-3 rounded-xl font-semibold transition"
          >
            Return to Homepage
          </Link>
        </div>
        
        <p className="text-sm text-gray-500 mt-8">
          Questions? Email us at{' '}
          <a href="mailto:hello@stencilwash.com" className="text-primary-500 hover:underline">
            hello@stencilwash.com
          </a>
        </p>
      </div>
    </main>
  );
}