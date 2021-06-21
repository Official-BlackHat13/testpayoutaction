import com.icicibank.instapayment.security.ENCRYPTION;

class EncryptData{
    public static void main(String[] s)
    {
        System.out.println(s[0]);
        try{
        System.out.println(String.valueOf(ENCRYPTION.encryptInstaPaymnentData(s[0].trim(),s[1])));
        }
        catch(Exception e)
        {
            System.out.println(e);
        }
        
    }
}