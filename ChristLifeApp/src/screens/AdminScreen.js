import React, { useState, useEffect, useContext } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, ActivityIndicator } from 'react-native';
import { collection, getDocs, doc, updateDoc } from 'firebase/firestore';
import { db } from '../config/firebase';
import { AuthContext } from '../context/AuthContext';

const AdminScreen = ({ navigation }) => {
  const { user } = useContext(AuthContext);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Security check: if not admin, kick them back to home
    if (!user || user.role !== 'admin') {
      setMessage('⛔ Access Denied. Admins only.');
      setLoading(false);
      return;
    }
    fetchUsers();
  }, [user]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const querySnapshot = await getDocs(collection(db, 'users'));
      const userList = querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      setUsers(userList);
    } catch (error) {
      setMessage('❌ Error fetching users: ' + error.message);
    }
    setLoading(false);
  };

  const updateUserStatus = async (userId, newRole, isApproved) => {
    setMessage('Updating...');
    try {
      await updateDoc(doc(db, 'users', userId), {
        role: newRole,
        approved: isApproved
      });
      setMessage('✅ User updated successfully!');
      fetchUsers(); // Refresh the list
    } catch (error) {
      setMessage('❌ Error: ' + error.message);
    }
  };

  const renderUser = ({ item }) => (
    <View style={styles.userCard}>
      <Text style={styles.userName}>{item.name}</Text>
      <Text style={styles.userEmail}>{item.email}</Text>
      <Text style={styles.userStatus}>
        Role: {item.role} | Status: {item.approved ? '✅ Approved' : '⏳ Pending'}
      </Text>

      <View style={styles.buttonRow}>
        {!item.approved && (
          <TouchableOpacity 
            style={[styles.actionBtn, styles.approveBtn]} 
            onPress={() => updateUserStatus(item.id, item.role, true)}
          >
            <Text style={styles.btnText}>Approve</Text>
          </TouchableOpacity>
        )}
        
        <TouchableOpacity 
          style={[styles.actionBtn, styles.roleBtn]} 
          onPress={() => updateUserStatus(item.id, 'usher', item.approved)}
        >
          <Text style={styles.btnText}>Usher</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.actionBtn, styles.roleBtn]} 
          onPress={() => updateUserStatus(item.id, 'prayer', item.approved)}
        >
          <Text style={styles.btnText}>Prayer</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={[styles.actionBtn, styles.roleBtn]} 
          onPress={() => updateUserStatus(item.id, 'welfare', item.approved)}
        >
          <Text style={styles.btnText}>Welfare</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  if (loading) {
    return <ActivityIndicator size="large" color="#4A90E2" style={{ flex: 1, justifyContent: 'center' }} />;
  }

  // If access is denied, show this instead of the list
  if (user?.role !== 'admin') {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>{message || '⛔ Access Denied'}</Text>
        <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
          <Text style={styles.backBtnText}>⬅️ Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Admin Dashboard</Text>
      
      {message ? <Text style={styles.messageBox}>{message}</Text> : null}

      <TouchableOpacity 
        style={styles.backBtn} 
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.backBtnText}>⬅️ Back to Home</Text>
      </TouchableOpacity>

      {/* NEW: POST ANNOUNCEMENT BUTTON */}
      <TouchableOpacity 
        style={styles.postBtn} 
        onPress={() => navigation.navigate('CreateAnnouncement')}
      >
        <Text style={styles.postBtnText}>📢 Post New Announcement</Text>
      </TouchableOpacity>

      <FlatList
        data={users}
        keyExtractor={item => item.id}
        renderItem={renderUser}
        contentContainerStyle={{ paddingBottom: 20 }}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5', padding: 20 },
  header: { fontSize: 24, fontWeight: 'bold', color: '#333', marginBottom: 20, textAlign: 'center' },
  errorText: { fontSize: 20, color: '#E24A4A', fontWeight: 'bold', textAlign: 'center', marginTop: 50 },
  messageBox: { backgroundColor: '#E5FFF0', color: '#2ECC71', padding: 10, borderRadius: 5, textAlign: 'center', marginBottom: 15, fontWeight: 'bold' },
  backBtn: { backgroundColor: '#666', padding: 12, borderRadius: 8, alignItems: 'center', marginBottom: 15 },
  backBtnText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
  postBtn: { backgroundColor: '#4A90E2', padding: 12, borderRadius: 8, alignItems: 'center', marginBottom: 20 },
  postBtnText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
  userCard: { backgroundColor: '#fff', padding: 15, borderRadius: 10, marginBottom: 15, shadowColor: '#000', shadowOpacity: 0.1, shadowRadius: 5, elevation: 3 },
  userName: { fontSize: 18, fontWeight: 'bold', color: '#333' },
  userEmail: { fontSize: 14, color: '#666', marginBottom: 5 },
  userStatus: { fontSize: 14, color: '#4A90E2', fontWeight: '600', marginBottom: 10 },
  buttonRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  actionBtn: { paddingVertical: 10, paddingHorizontal: 12, borderRadius: 6, flex: 1, minWidth: '30%', alignItems: 'center' },
  approveBtn: { backgroundColor: '#2ECC71' },
  roleBtn: { backgroundColor: '#4A90E2' },
  btnText: { color: '#fff', fontWeight: 'bold', fontSize: 13 }
});

export default AdminScreen;