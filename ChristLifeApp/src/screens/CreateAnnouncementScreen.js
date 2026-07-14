import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import { db } from '../config/firebase';

const CreateAnnouncementScreen = ({ navigation }) => {
  const [title, setTitle] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');

  const handlePost = async () => {
    if (!title || !message) {
      setStatusMsg(' Please fill in both title and message.');
      return;
    }

    setLoading(true);
    setStatusMsg('');
    try {
      await addDoc(collection(db, 'announcements'), {
        title: title,
        message: message,
        createdAt: serverTimestamp()
      });
      setStatusMsg('✅ Announcement posted successfully!');
      setTitle('');
      setMessage('');
    } catch (error) {
      setStatusMsg('❌ Error: ' + error.message);
    }
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Post New Announcement</Text>

      {statusMsg ? <Text style={styles.statusMsg}>{statusMsg}</Text> : null}

      <Text style={styles.label}>Title</Text>
      <TextInput 
        style={styles.input} 
        placeholder="e.g., Sunday Service Time Change" 
        value={title} 
        onChangeText={setTitle} 
      />

      <Text style={styles.label}>Message</Text>
      <TextInput 
        style={[styles.input, styles.textArea]} 
        placeholder="Type your announcement here..." 
        value={message} 
        onChangeText={setMessage} 
        multiline={true}
        numberOfLines={6}
      />

      {loading ? (
        <ActivityIndicator size="large" color="#4A90E2" style={{ marginTop: 20 }} />
      ) : (
        <TouchableOpacity style={styles.postBtn} onPress={handlePost}>
          <Text style={styles.postBtnText}>📢 Post Announcement</Text>
        </TouchableOpacity>
      )}

      <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
        <Text style={styles.backBtnText}>⬅️ Back to Admin Dashboard</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5', padding: 20 },
  header: { fontSize: 24, fontWeight: 'bold', color: '#333', marginBottom: 20, textAlign: 'center' },
  label: { fontSize: 16, fontWeight: '600', color: '#333', marginBottom: 5, marginTop: 10 },
  input: { backgroundColor: '#fff', borderWidth: 1, borderColor: '#ddd', padding: 15, borderRadius: 8, fontSize: 16 },
  textArea: { height: 120, textAlignVertical: 'top' },
  statusMsg: { backgroundColor: '#E5FFF0', color: '#2ECC71', padding: 10, borderRadius: 5, textAlign: 'center', marginBottom: 15, fontWeight: 'bold' },
  postBtn: { backgroundColor: '#4A90E2', padding: 15, borderRadius: 8, alignItems: 'center', marginTop: 20 },
  postBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  backBtn: { backgroundColor: '#666', padding: 12, borderRadius: 8, alignItems: 'center', marginTop: 20 },
  backBtnText: { color: '#fff', fontWeight: 'bold', fontSize: 16 }
});

export default CreateAnnouncementScreen;