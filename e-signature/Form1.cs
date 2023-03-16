using System;
using System.Windows.Forms;
using System.Numerics;
using System.IO;
using System.Text;

namespace Esignature
{
    public partial class Form1 : Form
    {
        private DigitalSignature ds = new DigitalSignature();
        private BigInteger d;
        Gost_34_11_2018 G256 = new Gost_34_11_2018(256);

        public Form1()
        {
            InitializeComponent();
        }

        private string addZero(string str, int num)
        {
            while (str.Length % num != 0)
                str = "0" + str;
            return str;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (textBox7.Text == "")
                MessageBox.Show("Введите текст!", "Ошибка!");
            else
            {
                string text = textBox7.Text;
                byte[] text_byte = Encoding.UTF8.GetBytes(text);

                if (textBox1.Text == "")
                    MessageBox.Show("Введите ключ подписи!", "Ошибка!");
                else
                {
                    d = BigInteger.Parse(textBox1.Text);

                    // Формирование ключа проверки подписи.
                    EllipticCurve.EllipticCurvePoint Q = ds.G.scalMultNumByPointEC(d);
                    StreamWriter f = new StreamWriter("signatureVerificationKey.txt");
                    f.WriteLine("X: " + Q.x.ToString() + "\nY: " + Q.y.ToString());
                    f.Close();

                    BigInteger signature = BigInteger.Parse(ds.ToFormDigitalSignature(text_byte, d));

                    textBox2.Text = signature.ToString("X");
                }
            }
        }

        private void button5_Click(object sender, EventArgs e)
        {
            textBox8.Text = "";
            textBox3.Text = "";
            textBox6.Text = "";
            textBox4.Text = "";
            textBox5.Text = "";
            label10.Text = "";
        }

        private void button6_Click(object sender, EventArgs e)
        {
            textBox7.Text = "";
            textBox1.Text = "";
            textBox2.Text = "";
            label9.Text = "";
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (textBox8.Text == "")
                MessageBox.Show("Введите текст!", "Ошибка!");
            else
            {
                string text = textBox8.Text;
                byte[] text_byte = Encoding.UTF8.GetBytes(text);

                if (textBox3.Text == "" || textBox6.Text == "")
                    MessageBox.Show("Введите ключ проверки подписи!", "Ошибка!");
                else
                {
                    if (textBox4.Text == "")
                        MessageBox.Show("Введите ЭЦП!", "Ошибка!");
                    else
                    {
                        EllipticCurve.EllipticCurvePoint Q = new EllipticCurve.EllipticCurvePoint(BigInteger.Parse(textBox3.Text), BigInteger.Parse(textBox6.Text));
                        BigInteger sig = BigInteger.Parse(textBox4.Text, System.Globalization.NumberStyles.HexNumber);
                        string signature = sig.ToString();
                        signature = addZero(signature, 256 * 2);
                        bool res = ds.ToVerifyDigitalSignature(text_byte, signature, Q);
                        textBox5.Text = res.ToString();
                    }
                }
            }
        }

        private void button4_Click(object sender, EventArgs e)
        {
            if (textBox9.Text == "")
                MessageBox.Show("Введите текст!", "Ошибка!");
            else
            {
                string text = textBox9.Text;
                byte[] text_byte = Encoding.UTF8.GetBytes(text);

                byte[] hash = G256.GetHash(text_byte);

                string s = "";
                for (int i = 0; i < hash.Length; i++)
                    s += hash[i].ToString("X");

                textBox10.Text = s;
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            textBox9.Text = "";
            textBox10.Text = "";
        }
    }
    public class DigitalSignature
    {
        Gost_34_11_2018 G256 = new Gost_34_11_2018(256);
        EllipticCurve.EllipticCurvePoint C;
        public EllipticCurve.EllipticCurvePoint G = new EllipticCurve.EllipticCurvePoint(EllipticCurve.EllipticCurve.x_G, EllipticCurve.EllipticCurve.y_G);
        BigInteger n = EllipticCurve.EllipticCurve.n;
        BigInteger e;

        public string ToFormDigitalSignature(byte[] array, BigInteger signatureKey)
        {
            byte[] hash = G256.GetHash(array);

            BigInteger alpha = 0, k, r, s;
            Random rnd = new Random();

            for (int i = 0; i < hash.Length; i++)
                alpha += hash[i] * (BigInteger)(Math.Pow(2, i));

            e = alpha % n;
            if (e == 0) e = 1;

            while (true)
            {
                k = rnd.Next(0, n);
                if (k == 0 || k == n) continue;

                C = G.scalMultNumByPointEC(k);
                r = C.x % n;
                if (r == 0) continue;
                s = (r * signatureKey + k * e) % n;
                if (s == 0) continue;
                break;
            }

            string r_vector = r.ToBinaryString(256);
            string s_vector = s.ToBinaryString(256);

            return r_vector + s_vector;
        }

        BigInteger[] gcdex(BigInteger a, BigInteger b)
        {
            if (a == 0)
                return new BigInteger[] { b, 0, 1 };
            BigInteger[] gcd = gcdex(b % a, a);
            return new BigInteger[] { gcd[0], gcd[2] - (b / a) * gcd[1], gcd[1] };
        }

        BigInteger invmod(BigInteger a, BigInteger m)
        {
            BigInteger[] g = gcdex(a, m);
            if (g[0] > 1)
                return BigInteger.Zero;
            else
                return (g[1] % m + m) % m;
        }

        public bool ToVerifyDigitalSignature(byte[] array, string digitalSignature, EllipticCurve.EllipticCurvePoint signatureVerificationKey)
        {
            BigInteger r = digitalSignature.Substring(0, 256).FromBinary();
            BigInteger s = digitalSignature.Substring(256).FromBinary();

            if ((!(r > 0 && r < n)) || (!(s > 0 && s < n)))
                return false;

            byte[] hash = G256.GetHash(array);

            BigInteger alpha = 0;

            for (int k = 0; k < hash.Length; k++)
                alpha += hash[k] * (BigInteger)Math.Pow(2, k);

            e = alpha % n;
            if (e == 0) e = 1;

            BigInteger v = invmod(e, n);
            BigInteger z1, z2;

            z1 = (s * v) % n;
            z2 = ((n - r) * v) % n;

            C = G.scalMultNumByPointEC(z1).addingPoint(signatureVerificationKey.scalMultNumByPointEC(z2));

            BigInteger R = C.x % n;

            if (R == r)
                return true;
            
            return false;
        }
    }

    public static class RandomExtension
    {
        public static BigInteger Next(this Random random, BigInteger minValue, BigInteger maxValue)
        {
            int number_digits_min = minValue.ToString().Length, number_digits_max = maxValue.ToString().Length;
            int number_digits_in_num = random.Next(number_digits_min, number_digits_max);
            string num = "";
            int digit;

            for (int i = 0; i < number_digits_in_num; i++)
            {
                digit = random.Next(0, 10);
                num += digit.ToString();
            }
            return BigInteger.Parse(num);
        }
    }

    public static class BigIntegerExtension
    {
        public static string ToBinaryString(this BigInteger bigint, int maxNumOfDigits)
        {
            byte[] bytes = bigint.ToByteArray();
            int idx = bytes.Length - 1;

            StringBuilder base2 = new StringBuilder(bytes.Length * 8);
            string binary = Convert.ToString(bytes[idx], 2);

            base2.Append(binary);
            
            for (idx--; idx >= 0; idx--)
                base2.Append(Convert.ToString(bytes[idx], 2).PadLeft(8, '0'));
            
            int diff = maxNumOfDigits - base2.Length;

            string zero = "";

            for (int i = 0; i < diff; i++)
                zero += "0";

            if (diff < 0)
                base2.Remove(0, Math.Abs(diff));

            return zero + base2.ToString();
        }
    }

    public static class StringExtension
    {
        public static BigInteger FromBinary(this string input)
        {
            BigInteger big = new BigInteger();
            foreach (var c in input)
            {
                big <<= 1;
                big += c - '0';
            }

            return big;
        }
    }
}