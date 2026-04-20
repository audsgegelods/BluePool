import { useState, useEffect, useRef } from 'react'
import api from '../api'

import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Stack from '@mui/material/Stack'
import CircularProgress from '@mui/material/CircularProgress'

function ChatBox({ rideId, currentUserId }) {
    const [messages, setMessages] = useState([])
    const [newMessage, setNewMessage] = useState('')
    const [loading, setLoading] = useState(true)
    const [sending, setSending] = useState(false)
    const messagesEndRef = useRef(null)

    useEffect(() => {
        fetchMessages()
    }, [rideId])

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const fetchMessages = async () => {
        setLoading(true)
        try {
            const res = await api.get(`/rideposting/api/ride/${rideId}/messages/`)
            setMessages(res.data)
        } catch (err) {
            console.error('Failed to fetch messages', err)
        } finally {
            setLoading(false)
        }
    }

    const sendMessage = async (e) => {
        e.preventDefault()
        if (!newMessage.trim()) return
        setSending(true)
        try {
            const res = await api.post(`/rideposting/api/ride/${rideId}/messages/`, {
                text: newMessage
            })
            setMessages([...messages, res.data])
            setNewMessage('')
        } 
        catch (err) {
            alert('Failed to send message')
        } 
        finally {
            setSending(false)
        }
    }

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    if (loading) {
        return <Box sx={{ textAlign: 'center', py: 2 }}><CircularProgress size={24} /></Box>
    }

    return (
        <Box sx={{ mt: 3 }}>
            <h3 style={{ color: 'white', marginBottom: '12px' }}>Chat</h3>
            <Box sx={{
                backgroundColor: '#1a2a4a',
                borderRadius: '4px',
                padding: '12px',
                maxHeight: '300px',
                overflowY: 'auto',
                mb: 2
            }}>
                {messages.length === 0 ? (
                    <p style={{ color: '#ffffff', textAlign: 'center' }}>No messages yet.</p>
                ) : (
                    messages.map((msg) => (
                        <div key={msg.id} style={{
                            marginBottom: '12px',
                            textAlign: msg.author?.id === currentUserId ? 'right' : 'left'
                        }}>
                            <div style={{
                                display: 'inline-block',
                                backgroundColor: msg.author?.id === currentUserId ? '#0a1a3a' : '#2a3a5a',
                                padding: '8px 12px',
                                borderRadius: '12px',
                                maxWidth: '80%'
                            }}>
                                <small style={{ color: '#aaa', fontSize: '0.7rem' }}>
                                    {msg.author?.username || 'Unknown'} • {new Date(msg.time).toLocaleTimeString()}
                                </small>
                                <p style={{ margin: '4px 0 0', color: 'white' }}>{msg.text}</p>
                            </div>
                        </div>
                    ))
                )}
                <div ref={messagesEndRef} />
            </Box>

            <form onSubmit={sendMessage}>
                <Stack direction="row" spacing={1}>
                    <TextField
                        fullWidth
                        size="small"
                        variant="outlined"
                        placeholder="Type a message..."
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        disabled={sending}
                        sx={{ bgcolor: 'white', borderRadius: 1 }}
                    />
                    <Button type="submit" variant="contained" disabled={sending || !newMessage.trim()}
                        sx={{ color: 'white', '&.Mui-disabled': { color: '#2a3a5a' } }}>
                        Send
                    </Button>
                </Stack>
            </form>
        </Box>
    )
}

export default ChatBox