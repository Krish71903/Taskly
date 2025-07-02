import React, { useState, useEffect } from 'react';

interface Email {
  id: number;
  subject: string;
  sender: string;
  date: string;
}

const Dashboard: React.FC = () => {
  const [emails, setEmails] = useState<Email[]>([]);
  const [schedulePrompt, setSchedulePrompt] = useState('');

  useEffect(() => {
    // Fetch recent emails from the backend
    const fetchEmails = async () => {
      // const response = await fetch('http://localhost:8000/emails/recent');
      // const data = await response.json();
      // setEmails(data);
      // Mock data for now:
      setEmails([
        { id: 1, subject: 'Meeting Confirmation', sender: 'john.doe@example.com', date: '2024-06-28' },
        { id: 2, subject: 'Project Update', sender: 'jane.smith@example.com', date: '2024-06-28' },
        { id: 3, subject: 'Invoice #12345', sender: 'accounting@example.com', date: '2024-06-27' },
      ]);
    };

    fetchEmails();
  }, []);

  const handleSchedule = () => {
    console.log(`Scheduling: ${schedulePrompt}`);
    // Call backend to schedule
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      
      {/* Smart scheduling bar */}
      <div className="mb-8">
        <input
          type="text"
          value={schedulePrompt}
          onChange={(e) => setSchedulePrompt(e.target.value)}
          placeholder="Schedule a meeting with John Friday at 2pm"
          className="w-full p-2 border rounded"
        />
        <button onClick={handleSchedule} className="bg-blue-500 text-white p-2 rounded mt-2">
          Schedule
        </button>
      </div>

      {/* Email list */}
      <div>
        <h2 className="text-2xl font-bold mb-4">Recent Emails</h2>
        <ul>
          {emails.map(email => (
            <li key={email.id} className="border-b p-2 flex justify-between items-center">
              <div>
                <span className="font-bold">{email.sender}</span> - {email.subject}
              </div>
              <div>
                <button className="bg-green-500 text-white p-1 rounded mr-2">Summarize</button>
                <button className="bg-yellow-500 text-white p-1 rounded">Draft Reply</button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard; 