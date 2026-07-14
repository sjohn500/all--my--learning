import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, ActivityIndicator } from 'react-native';
import { collection, getDocs, query, orderBy } from 'firebase/firestore';
import { db } from '../config/firebase';

const AnnouncementsScreen = ({ navigation }) => {
  const [announcements, setAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnnouncements();
  }, []);

  const fetchAnnouncements = async () => {
    setLoading(true);
    try {
      // Get announcements, ordered by date (newest first)
      const q = query(collection(db, 'announcements'), orderBy('createdAt', 'desc'));
      const querySnapshot = await getDocs(q);
      const list = querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      setAnnouncements(list);
    } catch (error) {
      console.error("Error fetching announcements:", error);
    }
    setLoading(false);
  };

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <Text style={styles.title}>{item.title}</Text>
      <Text style={styles.message}>{item.message}</Text>
      <Text style={styles.date}>
        Posted on: {item.createdAt ? new Date(item.createdAt.seconds * 1000).toLocaleDateString() : 'Recently'}
      </Text>
    </View>
  );

  if (loading) {
    return <ActivityIndicator size="large" color="#4A90E2" style={{ flex: 1, justifyContent: 'center' }} />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Church Announcements</Text>
      
      {announcements.length === 0 ? (
        <Text style={styles.emptyText}>No announcements yet. Check back soon!</Text>
      ) : (
        <FlatList
          data={announcements}
          keyExtractor={item => item.id}
          renderItem={renderItem}
          contentContainerStyle={{ paddingBottom: 20 }}
        />
      )}

      <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
        <Text style={styles.backBtnText}>⬅️ Back to Home</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5', padding: 20 },
  header: { fontSize: 24, fontWeight: 'bold', color: '#333', marginBottom: 20, textAlign: 'center' },
  emptyText: { fontSize: 16, color: '#666', textAlign: 'center', marginTop: 50 },
  card: { backgroundColor: '#fff', padding: 20, borderRadius: 10, marginBottom: 15, shadowColor: '#000', shadowOpacity: 0.1, shadowRadius: 5, elevation: 3, borderLeftWidth: 5, borderLeftColor: '#4A90E2' },
  title: { fontSize: 18, fontWeight: 'bold', color: '#333', marginBottom: 10 },
  message: { fontSize: 16, color: '#555', lineHeight: 24, marginBottom: 10 },
  date: { fontSize: 12, color: '#999', fontStyle: 'italic' },
  backBtn: { backgroundColor: '#666', padding: 12, borderRadius: 8, alignItems: 'center', marginTop: 10 },
  backBtnText: { color: '#fff', fontWeight: 'bold', fontSize: 16 }
});

export default AnnouncementsScreen;