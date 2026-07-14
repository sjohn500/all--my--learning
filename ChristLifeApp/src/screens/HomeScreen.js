import React, { useContext } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { AuthContext } from '../context/AuthContext';
import { signOut } from 'firebase/auth';
import { auth } from '../config/firebase';

const HomeScreen = ({ navigation }) => {
  const { user } = useContext(AuthContext);

  const handleLogout = async () => {
    await signOut(auth);
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.welcome}>Welcome,</Text>
      <Text style={styles.name}>{user?.name || user?.email}</Text>
      
      <View style={styles.card}>
        <Text style={styles.label}>Role:</Text>
        <Text style={styles.value}>{user?.role ? user.role.toUpperCase() : 'MEMBER'}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.label}>Status:</Text>
        <Text style={[styles.value, { color: user?.approved ? '#2ECC71' : '#E24A4A' }]}>
          {user?.approved ? '✅ Approved' : '⏳ Pending Approval'}
        </Text>
      </View>

      {/* THIS IS THE MAGIC BUTTON THAT ONLY SHOWS FOR ADMINS */}
      {user?.role === 'admin' && (
        <TouchableOpacity 
          style={styles.adminBtn} 
          onPress={() => navigation.navigate('Admin')}
        >
          <Text style={styles.adminBtnText}>⚙️ Open Admin Dashboard</Text>
        </TouchableOpacity>
      )}

      {/* NEW: ANNOUNCEMENTS BUTTON (Visible to everyone) */}
      <TouchableOpacity 
        style={styles.announceBtn} 
        onPress={() => navigation.navigate('Announcements')}
      >
        <Text style={styles.announceBtnText}>📢 View Announcements</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
        <Text style={styles.logoutText}>Logout</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: { flexGrow: 1, justifyContent: 'center', alignItems: 'center', padding: 20, backgroundColor: '#fff' },
  welcome: { fontSize: 20, color: '#666' },
  name: { fontSize: 32, fontWeight: 'bold', color: '#333', marginBottom: 30, textAlign: 'center' },
  card: { backgroundColor: '#f9f9f9', padding: 20, borderRadius: 10, width: '100%', marginBottom: 15, alignItems: 'center', borderWidth: 1, borderColor: '#eee' },
  label: { fontSize: 14, color: '#888', marginBottom: 5 },
  value: { fontSize: 20, fontWeight: 'bold', color: '#333' },
  adminBtn: { backgroundColor: '#333', padding: 15, borderRadius: 8, width: '100%', alignItems: 'center', marginTop: 20 },
  adminBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  announceBtn: { backgroundColor: '#4A90E2', padding: 15, borderRadius: 8, width: '100%', alignItems: 'center', marginTop: 15 },
  announceBtnText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  logoutBtn: { marginTop: 20, backgroundColor: '#E24A4A', padding: 15, borderRadius: 8, width: '100%', alignItems: 'center' },
  logoutText: { color: '#fff', fontSize: 18, fontWeight: 'bold' }
});

export default HomeScreen;