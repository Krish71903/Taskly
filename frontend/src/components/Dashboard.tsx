import React, { useState, useEffect } from 'react';

interface Email {
  id: string;
  thread_id: string;
  subject: string;
  sender: string;
  date: string;
  to: string;
  body: string;
  body_html: string;
  body_text: string;
  snippet: string;
  label_ids: string[];
}

const Dashboard: React.FC = () => {
  const [emails, setEmails] = useState<Email[]>([]);
  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null);
  const [schedulePrompt, setSchedulePrompt] = useState('');
  const [loading, setLoading] = useState(true);
  const [showCompose, setShowCompose] = useState(false);

  useEffect(() => {
    // Fetch recent emails from the backend
    const fetchEmails = async () => {
      console.log('🔍 Starting to fetch emails...');
      setLoading(true);
      try {
        console.log('📡 Making API call to:', 'http://localhost:8000/emails/recent');
        const response = await fetch('http://localhost:8000/emails/recent');
        console.log('📊 Response status:', response.status);
        
        if (response.ok) {
          const data = await response.json();
          console.log('📧 Raw API response:', data);
          console.log('📧 Emails array:', data.emails);
          console.log('📧 Number of emails:', data.emails?.length);
          setEmails(data.emails);
        } else {
          console.error('❌ Failed to fetch emails:', response.status);
          // Fallback to empty array if API fails
          setEmails([]);
        }
      } catch (error) {
        console.error('💥 Error fetching emails:', error);
        // Fallback to empty array if API fails
        setEmails([]);
      } finally {
        setLoading(false);
        console.log('✅ Fetch emails completed');
      }
    };

    fetchEmails();
  }, []);

  const handleSchedule = () => {
    console.log(`Scheduling: ${schedulePrompt}`);
    // Call backend to schedule
  };

  const handleEmailClick = (email: Email) => {
    setSelectedEmail(email);
  };

  const handleBackToList = () => {
    setSelectedEmail(null);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return 'Today';
    if (diffDays === 2) return 'Yesterday';
    if (diffDays <= 7) return date.toLocaleDateString('en-US', { weekday: 'short' });
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4">
          <button 
            onClick={() => setShowCompose(true)}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium"
          >
            Compose
          </button>
        </div>
        
        <nav className="flex-1 px-4">
          <ul className="space-y-1">
            <li><a href="#" className="flex items-center px-3 py-2 text-gray-700 bg-red-50 rounded-lg font-medium">📧 Inbox</a></li>
            <li><a href="#" className="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">⭐ Starred</a></li>
            <li><a href="#" className="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">📤 Sent</a></li>
            <li><a href="#" className="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">📝 Drafts</a></li>
            <li><a href="#" className="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">🗑️ Trash</a></li>
          </ul>
        </nav>

        {/* Smart scheduling section */}
        <div className="p-4 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Quick Schedule</h3>
          <input
            type="text"
            value={schedulePrompt}
            onChange={(e) => setSchedulePrompt(e.target.value)}
            placeholder="Schedule meeting..."
            className="w-full p-2 text-xs border rounded"
          />
          <button 
            onClick={handleSchedule} 
            className="w-full bg-green-500 text-white p-1 rounded mt-1 text-xs"
          >
            Schedule
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {selectedEmail ? (
          /* Email Detail View */
          <div className="flex-1 flex flex-col bg-white h-0">
            {/* Fixed Header */}
            <div className="flex-shrink-0 border-b border-gray-200 p-4 flex items-center justify-between">
              <button 
                onClick={handleBackToList}
                className="text-gray-600 hover:text-gray-800"
              >
                ← Back to Inbox
              </button>
              <div className="flex space-x-2">
                <button className="bg-green-500 text-white px-3 py-1 rounded text-sm">Summarize</button>
                <button className="bg-yellow-500 text-white px-3 py-1 rounded text-sm">Draft Reply</button>
                <button className="bg-red-500 text-white px-3 py-1 rounded text-sm">Delete</button>
              </div>
            </div>
            
            {/* Scrollable Content */}
            <div className="flex-1 overflow-y-auto">
              <div className="p-6">
                <div className="max-w-4xl mx-auto">
                  <h1 className="text-2xl font-bold mb-4 break-words">{selectedEmail.subject}</h1>
                  <div className="mb-6 pb-4 border-b border-gray-200">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                      <div className="min-w-0">
                        <div className="font-medium break-words">{selectedEmail.sender}</div>
                        <div className="text-sm text-gray-600 break-words">to {selectedEmail.to}</div>
                      </div>
                      <div className="text-sm text-gray-500 whitespace-nowrap">{formatDate(selectedEmail.date)}</div>
                    </div>
                  </div>
                </div>
                
                {/* Email Content - Full Width */}
                <div className="email-content-container">
                  {selectedEmail.body_html ? (
                    <div 
                      className="email-html-content"
                      dangerouslySetInnerHTML={{ __html: selectedEmail.body_html }}
                    />
                  ) : (
                    <div className="max-w-4xl mx-auto whitespace-pre-wrap break-words text-gray-800 leading-relaxed">
                      {selectedEmail.body_text || selectedEmail.body}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* Email List View */
          <div className="flex-1 flex flex-col bg-white h-0">
            <div className="flex-shrink-0 border-b border-gray-200 p-4">
              <h1 className="text-xl font-semibold">Inbox</h1>
            </div>
            
            <div className="flex-1 overflow-y-auto">
              {loading ? (
                <div className="p-8 text-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
                  <p className="text-gray-600 mt-2">Loading your emails...</p>
                </div>
              ) : emails.length === 0 ? (
                <div className="p-8 text-center text-gray-600">
                  <p>No emails found. Make sure you've authenticated with Gmail.</p>
                </div>
              ) : (
                <div className="divide-y divide-gray-200">
                  {emails.map(email => (
                    <div 
                      key={email.id} 
                      onClick={() => handleEmailClick(email)}
                      className="p-4 hover:bg-gray-50 cursor-pointer border-l-4 border-transparent hover:border-blue-400 transition-all"
                    >
                      <div className="flex items-start justify-between min-w-0">
                        <div className="flex-1 min-w-0 mr-4">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm font-medium text-gray-900 truncate">
                              {email.sender.replace(/<.*>/, '').trim()}
                            </span>
                            <span className="text-xs text-gray-500 ml-2 whitespace-nowrap">
                              {formatDate(email.date)}
                            </span>
                          </div>
                          <div className="text-sm font-medium text-gray-700 mb-1 truncate">
                            {email.subject || '(no subject)'}
                          </div>
                          <div className="text-sm text-gray-500 truncate">
                            {email.snippet}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Compose Modal (placeholder) */}
      {showCompose && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96">
            <h2 className="text-lg font-bold mb-4">Compose Email</h2>
            <p className="text-gray-600">Compose functionality coming soon!</p>
            <button 
              onClick={() => setShowCompose(false)}
              className="mt-4 bg-gray-500 text-white px-4 py-2 rounded"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 