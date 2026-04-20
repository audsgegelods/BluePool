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
        } catch (err) {
            alert('Failed to send message')
        } finally {
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
            <p style={{ color: '#ffffff' }}>Chat</p>
            <Box sx={{
                backgroundColor: '#1a2a4a',
            }}>
                {messages.length === 0 ? (
                    <p style={{ color: '#ffffff', textAlign: 'center' }}>No messages yet.</p>
                ) : (
                    messages.map((msg) => (
                        <div key={msg.id} style={{
                            textAlign: msg.author?.id === currentUserId ? 'right' : 'left'
                        }}>
                            <div style={{
                                display: 'inline-block'
                            }}>
                                <small style={{ color: '#ffffff', fontSize: '0.7rem' }}>
                                    {msg.author?.username || 'Unknown'} • {new Date(msg.time).toLocaleTimeString()}
                                </small>
                                <p style={{ color: 'white' }}>{msg.text}</p>
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
                        sx={{ bgcolor: 'white' }}
                    />
                    <Button type="submit" variant="contained" disabled={sending || !newMessage.trim()}>
                        Send
                    </Button>
                </Stack>
            </form>
        </Box>
    )
}

export default ChatBox